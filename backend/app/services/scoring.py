"""
Deterministic Multi-Factor Scoring Engine.
Implements the 7-factor scoring formula (0-100) and explainable recommendation breakdowns.
Supports pluggable semantic similarity strategies via an abstract interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseSemanticSimilarityEngine(ABC):
    """Abstract base class for semantic similarity engines (deterministic skill overlap or future vector embeddings)."""

    @abstractmethod
    def calculate_similarity(self, resource_skills: List[str], target_gap_skills: List[str]) -> float:
        """Calculate similarity score between resource target skills and target gap skills (0.0 - 1.0)."""
        pass


class SkillOverlapSimilarityEngine(BaseSemanticSimilarityEngine):
    """Deterministic Jaccard skill-overlap similarity engine for Phase 3."""

    def calculate_similarity(self, resource_skills: List[str], target_gap_skills: List[str]) -> float:
        r_set = {s.lower() for s in (resource_skills or [])}
        g_set = {s.lower() for s in (target_gap_skills or [])}

        if not r_set or not g_set:
            return 0.0

        intersection = r_set.intersection(g_set)
        union = r_set.union(g_set)

        if not union:
            return 0.0

        return len(intersection) / float(len(union))


class ScoringEngine:
    """
    Multi-factor scoring engine applying weights:
    Score = 100 * (0.25*S_goal + 0.20*S_gap + 0.20*S_prereq + 0.15*S_semantic + 0.10*S_diff + 0.05*S_time + 0.05*S_quality)
    """

    WEIGHT_GOAL = 0.25
    WEIGHT_GAP = 0.20
    WEIGHT_PREREQ = 0.20
    WEIGHT_SEMANTIC = 0.15
    WEIGHT_DIFF = 0.10
    WEIGHT_TIME = 0.05
    WEIGHT_QUALITY = 0.05

    IMPORTANCE_WEIGHTS = {
        "critical": 1.0,
        "high": 0.75,
        "medium": 0.5,
        "optional": 0.25
    }

    def __init__(self, semantic_engine: BaseSemanticSimilarityEngine = None):
        self.semantic_engine = semantic_engine or SkillOverlapSimilarityEngine()

    def calculate_goal_relevance(self, resource_skills: List[str], career_skills: List[str]) -> float:
        """Calculate ratio of resource skills matching target career skills."""
        if not resource_skills or not career_skills:
            return 0.0

        r_set = {s.lower() for s in resource_skills}
        c_set = {s.lower() for s in career_skills}

        match_count = len(r_set.intersection(c_set))
        return match_count / float(len(r_set))

    def calculate_skill_gap_score(self, resource_skills: List[str], gap_report: Dict[str, Any]) -> float:
        """Calculate importance-weighted skill gap relevance score."""
        gaps_list = gap_report.get("skill_gaps", [])
        if not gaps_list or not resource_skills:
            return 0.0

        r_set = {s.lower() for s in resource_skills}
        total_score = 0.0
        match_count = 0

        for g in gaps_list:
            s_slug = g["skill_slug"].lower()
            if s_slug in r_set:
                match_count += 1
                importance = g.get("importance", "high").lower()
                imp_weight = self.IMPORTANCE_WEIGHTS.get(importance, 0.75)
                gap_val = g.get("gap", 0)

                # Normalized gap component (max gap 5)
                gap_ratio = min(gap_val, 5) / 5.0
                total_score += imp_weight * gap_ratio

        if match_count == 0:
            return 0.0

        # Normalize score over matching skills, capped at 1.0
        avg_score = total_score / float(match_count)
        return min(1.0, round(avg_score, 4))

    def calculate_difficulty_match(self, difficulty_level: str, learner_proficiencies: List[int]) -> float:
        """Map resource difficulty to learner's current proficiency in target skills."""
        diff = (difficulty_level or "intermediate").lower()

        if not learner_proficiencies:
            avg_prof = 0
        else:
            avg_prof = sum(learner_proficiencies) / len(learner_proficiencies)

        if avg_prof <= 1:
            matrix = {"beginner": 1.0, "intermediate": 0.5, "advanced": 0.1}
        elif avg_prof <= 3:
            matrix = {"beginner": 0.6, "intermediate": 1.0, "advanced": 0.6}
        else:
            matrix = {"beginner": 0.2, "intermediate": 0.7, "advanced": 1.0}

        return matrix.get(diff, 0.5)

    def calculate_time_fit(self, duration_hours: float, weekly_hours: int) -> float:
        """Calculate how naturally resource duration fits weekly available time budget."""
        if duration_hours <= 0:
            return 1.0

        wh = max(1, weekly_hours)
        ratio = duration_hours / float(wh)

        if ratio <= 1.0:
            return 1.0
        elif ratio <= 2.0:
            return 0.85
        elif ratio <= 4.0:
            return 0.60
        else:
            return 0.30

    def calculate_quality_score(self, rating: float) -> float:
        """Calculate resource quality score (neutral 0.75 if rating is null)."""
        if rating is None:
            return 0.75

        try:
            r = float(rating)
            return round(min(1.0, max(0.0, r / 5.0)), 2)
        except (ValueError, TypeError):
            return 0.75

    def score_candidate(
        self,
        candidate: Dict[str, Any],
        gap_report: Dict[str, Any],
        prereq_evaluation: Dict[str, Any],
        weekly_hours: int,
        career_skill_slugs: List[str],
        current_skills: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Score a single candidate resource and generate explainable score breakdown.
        """
        res_skills = candidate.get("skill_slugs", [])

        # Sub-factor calculations
        s_goal = self.calculate_goal_relevance(res_skills, career_skill_slugs)
        s_gap = self.calculate_skill_gap_score(res_skills, gap_report)
        s_prereq = float(prereq_evaluation.get("readiness_score", 1.0))

        # Target gap skill slugs
        gap_slugs = [g["skill_slug"] for g in gap_report.get("skill_gaps", []) if g.get("gap", 0) > 0]
        s_semantic = self.semantic_engine.calculate_similarity(res_skills, gap_slugs)

        learner_profs = [current_skills.get(s, 0) for s in res_skills]
        s_diff = self.calculate_difficulty_match(candidate.get("difficulty_level"), learner_profs)
        s_time = self.calculate_time_fit(candidate.get("duration_hours", 10.0), weekly_hours)
        s_quality = self.calculate_quality_score(candidate.get("rating"))

        weighted_sum = (
            self.WEIGHT_GOAL * s_goal +
            self.WEIGHT_GAP * s_gap +
            self.WEIGHT_PREREQ * s_prereq +
            self.WEIGHT_SEMANTIC * s_semantic +
            self.WEIGHT_DIFF * s_diff +
            self.WEIGHT_TIME * s_time +
            self.WEIGHT_QUALITY * s_quality
        )

        final_score = round(min(100.0, max(0.0, weighted_sum * 100.0)), 1)

        breakdown = {
            "goal_relevance": round(s_goal, 2),
            "skill_gap": round(s_gap, 2),
            "prerequisite_readiness": round(s_prereq, 2),
            "semantic_similarity": round(s_semantic, 2),
            "difficulty_match": round(s_diff, 2),
            "time_fit": round(s_time, 2),
            "quality": round(s_quality, 2)
        }

        # Generate explainable reason codes
        reason_codes = []
        if s_gap >= 0.5:
            reason_codes.append("fills_critical_skill_gap")
        if s_goal >= 0.5:
            reason_codes.append("matches_target_career")
        if s_prereq == 1.0:
            reason_codes.append("prerequisites_satisfied")
        elif s_prereq < 0.5:
            reason_codes.append("prerequisites_blocked")
        if s_time >= 0.8:
            reason_codes.append("fits_weekly_time")
        if s_quality >= 0.8:
            reason_codes.append("high_quality_resource")
        if s_diff >= 0.8:
            reason_codes.append("optimal_difficulty_match")

        if not reason_codes:
            reason_codes.append("general_career_alignment")

        return {
            "resource_id": candidate["id"],
            "slug": candidate["slug"],
            "title": candidate["title"],
            "provider": candidate["provider"],
            "resource_type": candidate.get("resource_type", "course"),
            "difficulty_level": candidate.get("difficulty_level", "intermediate"),
            "duration_hours": candidate.get("duration_hours", 0.0),
            "rating": candidate.get("rating"),
            "score": final_score,
            "breakdown": breakdown,
            "reason_codes": reason_codes,
            "target_skills": candidate.get("target_skills", []),
            "prerequisites": candidate.get("prerequisites", []),
            "missing_prerequisites": prereq_evaluation.get("missing_prerequisites", []),
            "readiness_status": prereq_evaluation.get("status", "ready")
        }
