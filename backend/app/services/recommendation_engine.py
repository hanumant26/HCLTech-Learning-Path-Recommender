"""
Core Recommendation Engine Service.
Orchestrates skill gap analysis, NetworkX prerequisite resolution, candidate retrieval,
multi-factor deterministic scoring, ranking, and personalized learning path roadmap generation.
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from backend.app.models.career import Career, CareerSkill
from backend.app.models.skill import Skill
from backend.app.services.skill_gap import SkillGapAnalyzer
from backend.app.services.prerequisite_engine import PrerequisiteEngine
from backend.app.services.candidate_retriever import CandidateRetriever
from backend.app.services.scoring import ScoringEngine, BaseSemanticSimilarityEngine
from backend.app.services.learning_path_generator import LearningPathGenerator
from backend.app.services.exceptions import (
    RecommendationEngineError,
    UnknownCareerError,
    InvalidProfileError,
    NoCandidateResourcesError
)


class RecommendationEngine:
    """Core recommendation brain orchestrating the end-to-end recommendation pipeline."""

    def __init__(self, semantic_engine: Optional[BaseSemanticSimilarityEngine] = None):
        self.skill_gap_analyzer = SkillGapAnalyzer()
        self.scoring_engine = ScoringEngine(semantic_engine=semantic_engine)
        self.learning_path_generator = LearningPathGenerator()

    def validate_and_normalize_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize input learner profile dictionary.
        """
        if not isinstance(profile_data, dict):
            raise InvalidProfileError("Profile data must be a dictionary.")

        target_career = profile_data.get("target_career") or profile_data.get("target_role")
        if not target_career or not str(target_career).strip():
            raise InvalidProfileError("Profile must specify a non-empty target_career or target_role.")

        weekly_hours = profile_data.get("weekly_hours")
        if weekly_hours is None:
            weekly_hours = 10
        try:
            weekly_hours = int(weekly_hours)
        except (ValueError, TypeError):
            raise InvalidProfileError(f"weekly_hours must be an integer, got: {weekly_hours}")

        if weekly_hours <= 0:
            raise InvalidProfileError("weekly_hours must be greater than zero.")

        raw_skills = profile_data.get("skills", {})
        if not isinstance(raw_skills, dict):
            if isinstance(raw_skills, list):
                # Handle list of dicts if passed as [{skill_id/slug: ..., level: ...}]
                converted_skills = {}
                for item in raw_skills:
                    if isinstance(item, dict):
                        s_name = item.get("skill_slug") or item.get("skill_name") or item.get("name")
                        lvl = item.get("proficiency_level") or item.get("level") or 1
                        if s_name:
                            converted_skills[str(s_name)] = int(lvl)
                raw_skills = converted_skills
            else:
                raw_skills = {}

        normalized_skills = {}
        for skill_name, level in raw_skills.items():
            try:
                lvl_int = int(level)
            except (ValueError, TypeError):
                raise InvalidProfileError(f"Invalid proficiency level '{level}' for skill '{skill_name}'. Must be an integer 0-5.")

            if lvl_int < 0 or lvl_int > 5:
                raise InvalidProfileError(f"Proficiency level for '{skill_name}' must be between 0 and 5, got: {lvl_int}")

            normalized_skills[str(skill_name).strip()] = lvl_int

        completed = profile_data.get("completed_resources", [])
        if not isinstance(completed, list):
            completed = []

        return {
            "target_career": str(target_career).strip(),
            "weekly_hours": weekly_hours,
            "skills": normalized_skills,
            "completed_resources": [str(c).strip() for c in completed],
            "preferred_learning_style": profile_data.get("preferred_learning_style", "mixed"),
            "interests": profile_data.get("interests", [])
        }

    def generate_recommendations(
        self,
        profile_data: Dict[str, Any],
        db: Session,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Execute the end-to-end recommendation pipeline.

        :param profile_data: Dict containing learner profile input
        :param db: SQLAlchemy Session connected to SQLite DB
        :param top_n: Maximum number of top recommendations to rank and return
        :return: Complete recommendation result dict including skill gap report, ranked recommendations, and roadmap
        """
        # Step 1: Validate and normalize profile
        norm_profile = self.validate_and_normalize_profile(profile_data)
        target_career = norm_profile["target_career"]
        weekly_hours = norm_profile["weekly_hours"]
        user_skills = norm_profile["skills"]
        completed_resources = norm_profile["completed_resources"]

        # Step 2: Skill Gap Analysis
        gap_report = self.skill_gap_analyzer.analyze_gaps(
            target_career=target_career,
            current_skills=user_skills,
            db=db
        )

        # Step 3: Prerequisite Engine Resolution
        prereq_engine = PrerequisiteEngine(db=db)

        # Build current skill level dict by slug for prerequisite graph
        # Map user input skill names/slugs to canonical database slugs
        canonical_user_skills = {}
        all_db_skills = db.query(Skill).all()
        skill_lookup = {}
        for s in all_db_skills:
            skill_lookup[s.slug.lower()] = s.slug
            skill_lookup[s.name.lower()] = s.slug

        for k, v in user_skills.items():
            matched_slug = skill_lookup.get(k.lower(), k.lower())
            canonical_user_skills[matched_slug] = v

        # Identify missing prerequisites across all gap skills
        all_missing_prereq_slugs = set()
        for g in gap_report["skill_gaps"]:
            if g["gap"] > 0:
                prereq_check = prereq_engine.check_prerequisites_satisfied(
                    skill_slug=g["skill_slug"],
                    current_skills=canonical_user_skills
                )
                for mp in prereq_check.get("missing_prerequisites", []):
                    all_missing_prereq_slugs.add(mp["skill_slug"])

        # Step 4: Candidate Resource Retrieval
        retriever = CandidateRetriever(db=db)
        candidates = retriever.retrieve_candidates(
            gap_skills=gap_report["skill_gaps"],
            prerequisite_missing_skills=list(all_missing_prereq_slugs),
            completed_resources=completed_resources
        )

        # Step 5 & 6: Prerequisite Evaluation & Deterministic Multi-Factor Scoring
        scored_candidates = []
        career_skill_slugs = [g["skill_slug"] for g in gap_report["skill_gaps"]]

        for candidate in candidates:
            # Evaluate prerequisite readiness for candidate
            prereq_eval = prereq_engine.evaluate_resource_readiness(
                resource_target_skills=[(t["skill_slug"], t["level_gained"]) for t in candidate.get("target_skills", [])],
                resource_prerequisite_skills=candidate.get("prerequisites", []),
                current_skills=canonical_user_skills
            )

            # Calculate multi-factor score (0 - 100)
            scored_item = self.scoring_engine.score_candidate(
                candidate=candidate,
                gap_report=gap_report,
                prereq_evaluation=prereq_eval,
                weekly_hours=weekly_hours,
                career_skill_slugs=career_skill_slugs,
                current_skills=canonical_user_skills
            )
            scored_candidates.append(scored_item)

        # Step 7: Deterministic Ranking
        # Primary sort key: score descending. Secondary tie-breaker: resource_id ascending for 100% determinism.
        ranked_candidates = sorted(
            scored_candidates,
            key=lambda x: (-x["score"], x["resource_id"])
        )

        top_recommendations = ranked_candidates[:top_n]

        # Step 8: Learning Path Roadmap Generation
        roadmap = self.learning_path_generator.generate_roadmap(
            recommendations=top_recommendations,
            gap_report=gap_report,
            weekly_hours=weekly_hours
        )

        return {
            "target_career": gap_report["summary"]["career_title"],
            "career_slug": gap_report["summary"]["career_slug"],
            "weekly_hours": weekly_hours,
            "skill_gap_report": gap_report,
            "total_candidates_found": len(candidates),
            "recommendations": top_recommendations,
            "learning_path": roadmap
        }
