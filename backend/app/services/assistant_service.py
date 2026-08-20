"""
Phase 5: Conversational Assistant Service.

Provides natural language explanations and interactive guidance strictly grounded in the
deterministic recommendation pipeline outputs (skill gaps, 7-factor scores, prerequisite DAGs,
and multi-phase roadmaps).

Does NOT replace or recalculate scoring, prerequisite logic, or roadmap sequencing.
Supports Gemini LLM with automatic, robust deterministic fallback for offline/test resilience.
"""
import logging
import re
from typing import Any, Dict, List, Optional
import httpx
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.course import Course
from backend.app.services.recommendation_engine import RecommendationEngine
from backend.app.schemas.assistant import ChatMessage

logger = logging.getLogger(__name__)


class ConversationalAssistantService:
    """Service providing grounded conversational explanations over recommendation results."""

    def __init__(self, recommendation_engine: Optional[RecommendationEngine] = None):
        self.recommendation_engine = recommendation_engine or RecommendationEngine()

    def classify_intent(self, query: str, resource_slug: Optional[str] = None, is_resource_locked: bool = False) -> str:
        """
        Classify learner query into one of the core supported question types.
        """
        q = (query or "").lower().strip()

        if not q and resource_slug:
            return "why_locked" if is_resource_locked else "why_recommended"

        # 1. Prerequisite Skipping
        if any(re.search(p, q) for p in [r"\bskip\b", r"\bbypass\b", r"jump directly", r"without taking", r"can i avoid"]):
            return "skip_prerequisite"

        # 2. Locked / Access issues
        if any(re.search(p, q) for p in [r"\blocked\b", r"\bunlock\b", r"cannot access", r"why is.*blocked", r"not ready"]):
            return "why_locked"

        # 3. Why recommended / Course justification
        if any(re.search(p, q) for p in [r"why.*recommend", r"why.*suggest", r"why this", r"why should i take", r"reason for", r"how was this chosen"]):
            return "why_recommended"

        # 4. What next / Where to start
        if any(re.search(p, q) for p in [r"what.*next", r"where.*start", r"what should i learn", r"first step", r"begin with", r"start with", r"next course"]):
            return "what_next"

        # 5. Time budget / Limited time / Pacing
        if any(re.search(p, q) for p in [r"\btime\b", r"\bhours?\b", r"\bbusy\b", r"limited time", r"how long", r"schedule", r"pacing", r"weeks?", r"focus on"]):
            return "time_budget"

        # Default if resource is provided
        if resource_slug:
            return "why_locked" if is_resource_locked else "why_recommended"

        return "general_guidance"

    def build_grounding_context(
        self,
        profile_data: Dict[str, Any],
        db: Session,
        resource_slug: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate deterministic recommendation context for grounding.
        """
        recs_data = self.recommendation_engine.generate_recommendations(profile_data, db=db, top_n=10)

        # Locate specific resource if requested
        focused_resource = None
        if resource_slug:
            slug_lower = resource_slug.lower().strip()
            # Check in top recommendations
            for r in recs_data.get("recommendations", []):
                if r.get("slug", "").lower() == slug_lower or slug_lower in r.get("slug", "").lower() or slug_lower in r.get("title", "").lower():
                    focused_resource = r
                    break
            # Check in locked items
            if not focused_resource:
                for lk in recs_data.get("learning_path", {}).get("locked_items", []):
                    if lk.get("slug", "").lower() == slug_lower or slug_lower in lk.get("slug", "").lower() or slug_lower in lk.get("title", "").lower():
                        focused_resource = lk
                        break
            # Direct DB fallback if not in recommendations
            if not focused_resource:
                db_course = db.query(Course).filter((Course.slug == resource_slug) | (Course.slug.like(f"%{resource_slug}%"))).first()
                if db_course:
                    focused_resource = {
                        "resource_id": db_course.id,
                        "slug": db_course.slug,
                        "title": db_course.title,
                        "provider": db_course.provider,
                        "difficulty_level": db_course.difficulty_level,
                        "duration_hours": db_course.duration_hours,
                        "rating": db_course.rating,
                        "readiness_status": "ready",
                        "missing_prerequisites": [],
                        "reason_codes": ["catalog_resource"]
                    }

        return {
            "target_career": recs_data.get("target_career"),
            "career_slug": recs_data.get("career_slug"),
            "weekly_hours": recs_data.get("weekly_hours", 10),
            "skill_gap_report": recs_data.get("skill_gap_report", {}),
            "top_recommendations": recs_data.get("recommendations", []),
            "learning_path": recs_data.get("learning_path", {}),
            "focused_resource": focused_resource
        }

    def generate_chat_response(
        self,
        message: str,
        profile_data: Dict[str, Any],
        db: Session,
        resource_slug: Optional[str] = None,
        history: Optional[List[ChatMessage]] = None
    ) -> Dict[str, Any]:
        """
        Main entrypoint: Classifies intent, builds deterministic context, and generates grounded answer.
        """
        grounding = self.build_grounding_context(profile_data, db=db, resource_slug=resource_slug)

        is_locked = False
        if grounding.get("focused_resource"):
            is_locked = bool(grounding["focused_resource"].get("missing_prerequisites") or grounding["focused_resource"].get("readiness_status") == "blocked")

        intent = self.classify_intent(message, resource_slug=resource_slug, is_resource_locked=is_locked)

        # Determine referenced resources
        referenced_resources = []
        if resource_slug:
            referenced_resources.append(resource_slug)
        elif grounding.get("top_recommendations"):
            for r in grounding["top_recommendations"][:3]:
                referenced_resources.append(r["slug"])

        # Try Gemini LLM if API Key is configured
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
            try:
                answer = self._call_gemini_llm(
                    query=message,
                    intent=intent,
                    grounding=grounding,
                    history=history or []
                )
                if answer:
                    return {
                        "answer": answer,
                        "intent": intent,
                        "referenced_resources": referenced_resources,
                        "grounding_summary": self._summarize_grounding(grounding),
                        "engine": "gemini"
                    }
            except Exception as exc:
                logger.warning("Gemini LLM call failed or timed out: %s. Falling back to deterministic engine.", exc)

        # Fallback to deterministic rule-based explanation engine
        answer = self._generate_deterministic_explanation(
            intent=intent,
            query=message,
            grounding=grounding,
            resource_slug=resource_slug
        )

        return {
            "answer": answer,
            "intent": intent,
            "referenced_resources": referenced_resources,
            "grounding_summary": self._summarize_grounding(grounding),
            "engine": "deterministic-fallback"
        }

    def _summarize_grounding(self, grounding: Dict[str, Any]) -> Dict[str, Any]:
        """Create a compact summary of grounding metrics for verification."""
        summary = grounding.get("skill_gap_report", {}).get("summary", {})
        lp = grounding.get("learning_path", {})
        return {
            "target_career": grounding.get("target_career"),
            "readiness_percentage": summary.get("readiness_percentage"),
            "critical_gap_count": summary.get("critical_gap_count"),
            "total_estimated_weeks": lp.get("total_estimated_weeks"),
            "weekly_hours": grounding.get("weekly_hours"),
            "total_recommendations": len(grounding.get("top_recommendations", [])),
            "locked_items_count": len(lp.get("locked_items", []))
        }

    def _generate_deterministic_explanation(
        self,
        intent: str,
        query: str,
        grounding: Dict[str, Any],
        resource_slug: Optional[str] = None
    ) -> str:
        """
        Deterministic, rule-based explanation generator using verified backend data.
        """
        target_career = grounding.get("target_career", "your target career")
        weekly_hours = grounding.get("weekly_hours", 10)
        gap_summary = grounding.get("skill_gap_report", {}).get("summary", {})
        readiness = gap_summary.get("readiness_percentage", 0.0)
        recs = grounding.get("top_recommendations", [])
        lp = grounding.get("learning_path", {})
        phases = lp.get("phases", [])
        sequence = lp.get("sequence", [])
        locked_items = lp.get("locked_items", [])
        focused_resource = grounding.get("focused_resource")

        # -----------------------------------------------------------------
        # 1. WHY RECOMMENDED
        # -----------------------------------------------------------------
        if intent == "why_recommended":
            target_res = focused_resource or (recs[0] if recs else None)
            if not target_res:
                return f"Currently, no specific recommendations were found for **{target_career}** with your current profile settings."

            title = target_res.get("title", "this course")
            score = target_res.get("score", 0.0)
            breakdown = target_res.get("breakdown", {})
            reasons = target_res.get("reason_codes", [])
            skills = target_res.get("target_skills", [])
            skill_names = [s["skill_name"] if isinstance(s, dict) else str(s) for s in skills]

            reason_text_map = {
                "fills_critical_skill_gap": "Directly bridges one of your critical target skill gaps.",
                "matches_target_career": f"High alignment with the foundational requirements of {target_career}.",
                "prerequisites_satisfied": "All prerequisite skills are satisfied for your current level.",
                "fits_weekly_time": f"Fits comfortably within your {weekly_hours} hrs/week learning budget.",
                "optimal_difficulty_match": "Calibrated to your current level for effective progression.",
                "high_quality_resource": "High learner rating and proven pedagogical track record."
            }
            reason_bullets = "\n".join([f"- **{r.replace('_', ' ').title()}**: {reason_text_map.get(r, 'Directly benefits your target career path.')}" for r in reasons])

            return (
                f"### Why **{title}** is Recommended\n\n"
                f"**{title}** scored **{score}/100** on our multi-factor recommendation engine for **{target_career}**.\n\n"
                f"#### Key Factors:\n"
                f"{reason_bullets}\n\n"
                f"#### Score Breakdown:\n"
                f"- **Goal Relevance**: {int(breakdown.get('goal_relevance', 0) * 100)}%\n"
                f"- **Skill Gap Impact**: {int(breakdown.get('skill_gap', 0) * 100)}%\n"
                f"- **Prerequisite Readiness**: {int(breakdown.get('prerequisite_readiness', 0) * 100)}%\n"
                f"- **Time Budget Fit**: {int(breakdown.get('time_fit', 0) * 100)}%\n"
                f"- **Difficulty Calibration**: {int(breakdown.get('difficulty_match', 0) * 100)}%\n\n"
                f"**Skills You Will Gain**: {', '.join(skill_names) if skill_names else 'Core career competencies'}."
            )

        # -----------------------------------------------------------------
        # 2. WHY LOCKED
        # -----------------------------------------------------------------
        elif intent == "why_locked":
            target_res = focused_resource
            if not target_res and locked_items:
                target_res = locked_items[0]

            if not target_res or (not target_res.get("missing_prerequisites") and target_res.get("readiness_status") != "blocked"):
                return (
                    f"### Prerequisite Status: Unlocked\n\n"
                    f"This course currently has all prerequisites satisfied based on your profile and is ready to start!"
                )

            title = target_res.get("title", "This course")
            missing = target_res.get("missing_prerequisites", [])

            missing_lines = []
            for m in missing:
                if isinstance(m, dict):
                    missing_lines.append(f"- **{m.get('skill_name', m.get('skill_slug', 'Skill'))}**: Current level {m.get('current_level', 0)} (Required: Level {m.get('required_level', 1)})")
                else:
                    missing_lines.append(f"- **{m}**")

            return (
                f"### Why **{title}** is Locked\n\n"
                f"**{title}** is locked because the prerequisite engine detected unsatisfied foundational requirements.\n\n"
                f"#### Missing Prerequisites:\n"
                f"{chr(10).join(missing_lines) if missing_lines else '- Foundational prerequisite skills must be completed first.'}\n\n"
                f"#### How to Unlock:\n"
                f"1. Complete the Phase 1 foundational courses in your roadmap.\n"
                f"2. Once your prerequisite skill levels reach the required threshold, this course will automatically unlock as an actionable step."
            )

        # -----------------------------------------------------------------
        # 3. WHAT NEXT / WHERE TO START
        # -----------------------------------------------------------------
        elif intent == "what_next":
            if not sequence:
                return f"You currently do not have an active learning sequence for **{target_career}**. Please configure your skills profile to generate a roadmap."

            first_item = sequence[0]
            second_item = sequence[1] if len(sequence) > 1 else None

            response = (
                f"### What You Should Learn Next for **{target_career}**\n\n"
                f"Based on your current skill readiness of **{readiness}%**, start with **Phase 1**:\n\n"
                f"1. **Step 1: {first_item.get('title')}**\n"
                f"   - **Provider**: {first_item.get('provider')}\n"
                f"   - **Estimated Time**: {first_item.get('estimated_hours')} hours (~{max(1, round(first_item.get('estimated_hours', 10) / weekly_hours, 1))} weeks at {weekly_hours} hrs/wk)\n"
                f"   - **Target Skills**: {', '.join(first_item.get('target_skills', []))}\n"
            )
            if second_item:
                response += (
                    f"2. **Step 2: {second_item.get('title')}**\n"
                    f"   - **Provider**: {second_item.get('provider')}\n"
                    f"   - **Estimated Time**: {second_item.get('estimated_hours')} hours\n"
                    f"   - **Target Skills**: {', '.join(second_item.get('target_skills', []))}\n\n"
                )
            response += f"Following this sequence ensures you build required prerequisites step-by-step without hitting blocked courses."
            return response

        # -----------------------------------------------------------------
        # 4. SKIP PREREQUISITE
        # -----------------------------------------------------------------
        elif intent == "skip_prerequisite":
            return (
                f"### Can You Skip Prerequisites?\n\n"
                f"**We strongly advise against skipping prerequisites in your learning roadmap.**\n\n"
                f"#### Why Prerequisites Matter:\n"
                f"- **Concept Graph Dependency**: Advanced courses in **{target_career}** build directly on foundational concepts.\n"
                f"- **Downstream Bottlenecks**: Skipping foundational steps will leave downstream courses locked and make practical exercises significantly harder.\n"
                f"- **Time Efficiency**: Spending a few hours mastering the fundamentals prevents hours of troubleshooting in advanced projects.\n\n"
                f"If you already possess prior experience in a prerequisite skill, update your skill level in your profile to automatically unlock advanced modules."
            )

        # -----------------------------------------------------------------
        # 5. TIME BUDGET / LIMITED TIME
        # -----------------------------------------------------------------
        elif intent == "time_budget":
            total_weeks = lp.get("total_estimated_weeks", 0.0)
            total_hours = lp.get("total_estimated_hours", 0.0)

            first_phase = phases[0] if phases else None
            phase_items = first_phase.get("items", []) if first_phase else sequence[:2]

            item_bullets = "\n".join([f"- **{it.get('title')}** ({it.get('estimated_hours')} hrs)" for it in phase_items])

            return (
                f"### Pacing Guidance for **{weekly_hours} Hours/Week**\n\n"
                f"Your full roadmap for **{target_career}** spans **{total_hours} total hours** (~**{total_weeks} weeks** at your current commitment).\n\n"
                f"#### Recommended High-Impact Focus:\n"
                f"To maximize results with limited weekly time, focus strictly on Phase 1 core items:\n"
                f"{item_bullets}\n\n"
                f"#### Smart Study Strategy:\n"
                f"- Commit to consistent **{max(1, weekly_hours // 5)} hours per study session** rather than irregular cramming.\n"
                f"- Prioritize hands-on exercises that directly close critical skill gaps."
            )

        # -----------------------------------------------------------------
        # 6. GENERAL GUIDANCE
        # -----------------------------------------------------------------
        else:
            critical_gaps = gap_summary.get("critical_gap_count", 0)
            return (
                f"### Personalized Career Guidance for **{target_career}**\n\n"
                f"- **Current Readiness**: {readiness}%\n"
                f"- **Critical Skill Gaps**: {critical_gaps} skills need development\n"
                f"- **Weekly Commitment**: {weekly_hours} hours/week\n"
                f"- **Total Curriculum Duration**: ~{lp.get('total_estimated_weeks', 0)} weeks\n\n"
                f"You can ask me specific questions like:\n"
                f"- *'Why was [course name] recommended?'*\n"
                f"- *'Why is this course locked?'*\n"
                f"- *'What should I learn next?'*\n"
                f"- *'Can I skip prerequisites?'*\n"
                f"- *'How should I manage my limited weekly time?'*"
            )

    def _call_gemini_llm(
        self,
        query: str,
        intent: str,
        grounding: Dict[str, Any],
        history: List[ChatMessage]
    ) -> Optional[str]:
        """
        Call Gemini REST API with strict system prompt and verified grounding context.
        """
        system_instruction = (
            "You are the AI Learning Path Assistant for HCLTech's Personalized Learning Path Recommender. "
            "Your job is to explain recommendations, prerequisite requirements, time management, and roadmap sequence. "
            "CRITICAL RULES:\n"
            "1. ONLY use the provided verified backend data (skills, scores, score breakdowns, reason codes, prerequisites, locked items, roadmap phases).\n"
            "2. DO NOT invent or recommend courses, scores, or skill requirements that are not in the context.\n"
            "3. Explain mathematical score breakdowns and prerequisite dependencies in clear, friendly Markdown with bullet points.\n"
            "4. Keep explanations concise, professional, and encouraging."
        )

        context_str = (
            f"TARGET CAREER: {grounding.get('target_career')}\n"
            f"WEEKLY HOURS: {grounding.get('weekly_hours')}\n"
            f"READINESS PERCENTAGE: {grounding.get('skill_gap_report', {}).get('summary', {}).get('readiness_percentage')}%\n"
            f"SKILL GAPS: {grounding.get('skill_gap_report', {}).get('skill_gaps', [])}\n"
            f"TOP RECOMMENDATIONS: {grounding.get('top_recommendations', [])}\n"
            f"ROADMAP PHASES: {grounding.get('learning_path', {}).get('phases', [])}\n"
            f"ROADMAP SEQUENCE: {grounding.get('learning_path', {}).get('sequence', [])}\n"
            f"LOCKED ITEMS: {grounding.get('learning_path', {}).get('locked_items', [])}\n"
            f"FOCUSED RESOURCE: {grounding.get('focused_resource')}\n"
            f"DETECTED INTENT: {intent}\n"
        )

        # Build contents payload
        contents = []
        for h in history[-4:]:
            role = "user" if h.role == "user" else "model"
            contents.append({"role": role, "parts": [{"text": h.content}]})

        current_prompt = (
            f"Learner Context Data:\n{context_str}\n\n"
            f"Learner Question: {query}\n\n"
            f"Provide a clear, helpful response strictly based on the context data above."
        )
        contents.append({"role": "user", "parts": [{"text": current_prompt}]})

        payload = {
            "system_instruction": {"parts": [{"text": system_instruction}]},
            "contents": contents,
            "generationConfig": {
                "temperature": settings.LLM_TEMPERATURE,
                "maxOutputTokens": 800
            }
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.LLM_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"

        with httpx.Client(timeout=8.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text")
            else:
                logger.warning("Gemini API error (%d): %s", resp.status_code, resp.text)
                return None

        return None
