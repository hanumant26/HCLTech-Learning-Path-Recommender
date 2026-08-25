"""
Personalized Learning Path Generator.
Converts ranked recommendations and prerequisite relationships into an adaptive, ordered roadmap.
"""
from typing import Dict, List, Any
import math


class LearningPathGenerator:
    """Service to construct structured learning roadmaps with adaptive phases and time budgets."""

    def generate_roadmap(
        self,
        recommendations: List[Dict[str, Any]],
        gap_report: Dict[str, Any],
        weekly_hours: int
    ) -> Dict[str, Any]:
        """
        Generate an ordered, multi-phase learning path roadmap.

        :param recommendations: Ranked recommendations from ScoringEngine
        :param gap_report: Skill gap report from SkillGapAnalyzer
        :param weekly_hours: Learner's available weekly hours
        :return: Structured roadmap dict with adaptive phases, sequence order, and estimated timelines
        """
        wh = max(1, int(weekly_hours or 10))

        if not recommendations:
            return {
                "phases": [],
                "sequence": [],
                "total_items": 0,
                "total_estimated_hours": 0.0,
                "total_estimated_weeks": 0.0,
                "weekly_hours": wh
            }

        # Categorize candidates based on prerequisite readiness, resource type, difficulty, and skills
        foundational_items = []
        core_items = []
        applied_items = []
        project_capstone_items = []
        locked_items = []  # Resources with unsatisfied mandatory prerequisites — not actionable

        for rec in recommendations:
            res_type = (rec.get("resource_type") or "course").lower()
            diff = (rec.get("difficulty_level") or "intermediate").lower()
            readiness = rec.get("readiness_status", "ready")
            missing_prereqs = rec.get("missing_prerequisites", [])

            item = {
                "course_id": rec.get("resource_id"),
                "slug": rec["slug"],
                "title": rec["title"],
                "provider": rec.get("provider", ""),
                "item_type": res_type if res_type in ["project", "assessment"] else "course",
                "difficulty_level": diff,
                "estimated_hours": float(rec.get("duration_hours", 0.0)),
                "score": rec.get("score"),
                "readiness_status": readiness,
                "missing_prerequisites": missing_prereqs,
                "target_skills": [t["skill_name"] if isinstance(t, dict) else str(t) for t in rec.get("target_skills", [])],
                "reason_codes": rec.get("reason_codes", [])
            }

            # A resource with ANY unsatisfied mandatory prerequisite must never appear as an
            # immediate actionable step — it is locked until its prerequisites are completed.
            if missing_prereqs:
                locked_items.append(item)
            # Categorization into actionable phases (no missing prerequisites)
            elif readiness == "blocked" or diff == "beginner":
                foundational_items.append(item)
            elif res_type in ["project", "assessment"] or rec.get("is_project_based"):
                project_capstone_items.append(item)
            elif diff == "advanced":
                applied_items.append(item)
            else:
                core_items.append(item)

        # Dynamic phase construction (Skip empty phases naturally)
        phases = []
        seq_counter = 1

        # Phase 1: Foundations (Only if there are foundational or missing prerequisite items)
        if foundational_items:
            for item in foundational_items:
                item["sequence_order"] = seq_counter
                item["phase_number"] = 1
                item["phase_name"] = "Phase 1 — Foundations"
                seq_counter += 1
            phases.append({
                "phase_number": 1,
                "phase_name": "Phase 1 — Foundations",
                "items": foundational_items,
                "phase_hours": round(sum(i["estimated_hours"] for i in foundational_items), 1)
            })

        # Phase 2: Core Skills
        phase_2_number = 2 if foundational_items else 1
        if core_items:
            for item in core_items:
                item["sequence_order"] = seq_counter
                item["phase_number"] = phase_2_number
                item["phase_name"] = f"Phase {phase_2_number} — Core Skills"
                seq_counter += 1
            phases.append({
                "phase_number": phase_2_number,
                "phase_name": f"Phase {phase_2_number} — Core Skills",
                "items": core_items,
                "phase_hours": round(sum(i["estimated_hours"] for i in core_items), 1)
            })

        # Phase 3: Applied Learning
        phase_3_number = phase_2_number + (1 if core_items else 0)
        if applied_items:
            for item in applied_items:
                item["sequence_order"] = seq_counter
                item["phase_number"] = phase_3_number
                item["phase_name"] = f"Phase {phase_3_number} — Applied Learning"
                seq_counter += 1
            phases.append({
                "phase_number": phase_3_number,
                "phase_name": f"Phase {phase_3_number} — Applied Learning",
                "items": applied_items,
                "phase_hours": round(sum(i["estimated_hours"] for i in applied_items), 1)
            })

        # Phase 4: Projects / Capstone
        phase_4_number = phase_3_number + (1 if applied_items else 0)
        if project_capstone_items:
            for item in project_capstone_items:
                item["sequence_order"] = seq_counter
                item["phase_number"] = phase_4_number
                item["phase_name"] = f"Phase {phase_4_number} — Projects / Capstone"
                seq_counter += 1
            phases.append({
                "phase_number": phase_4_number,
                "phase_name": f"Phase {phase_4_number} — Projects / Capstone",
                "items": project_capstone_items,
                "phase_hours": round(sum(i["estimated_hours"] for i in project_capstone_items), 1)
            })

        # Combine all sequence items
        all_sequence_items = []
        for p in phases:
            all_sequence_items.extend(p["items"])

        total_hours = sum(item["estimated_hours"] for item in all_sequence_items)
        estimated_weeks = round(total_hours / float(wh), 1) if wh > 0 else 0.0

        return {
            "phases": phases,
            "sequence": all_sequence_items,
            "total_items": len(all_sequence_items),
            "total_estimated_hours": round(total_hours, 1),
            "total_estimated_weeks": estimated_weeks,
            "weekly_hours": wh,
            "locked_items": locked_items  # Blocked — prerequisites not yet satisfied
        }
