"""
Candidate Resource Retrieval Service.
Fetches learning resources from the database relevant to missing career skills and prerequisites,
excluding completed resources and duplicate entries.
"""
from typing import Dict, List, Set, Any
from sqlalchemy.orm import Session
from backend.app.models.course import Course, CourseSkill
from backend.app.models.skill import Skill
from backend.app.services.exceptions import NoCandidateResourcesError


class CandidateRetriever:
    """Service to retrieve relevant candidate courses from the SQLite database."""

    def __init__(self, db: Session):
        self.db = db

    def retrieve_candidates(
        self,
        gap_skills: List[Dict[str, Any]],
        prerequisite_missing_skills: List[str],
        completed_resources: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve candidate learning resources targeting missing skills or missing prerequisites.

        :param gap_skills: List of skill gap dicts from SkillGapAnalyzer
        :param prerequisite_missing_skills: List of missing prerequisite skill slugs
        :param completed_resources: List of completed course slugs or title strings to exclude
        :return: List of candidate resource dictionaries with associated skill details
        """
        # Build set of completed slugs/titles normalized to lowercase
        completed_set = {str(c).strip().lower() for c in (completed_resources or [])}

        # Target skill slugs of interest (gaps > 0 or missing prerequisites)
        target_slugs: Set[str] = set()

        for g in gap_skills:
            if g.get("gap", 0) > 0:
                target_slugs.add(g["skill_slug"].lower())

        for p_slug in prerequisite_missing_skills:
            target_slugs.add(p_slug.lower())

        if not target_slugs:
            # Learner has no gaps; fetch advanced or capstone resources targeting career skills
            for g in gap_skills:
                target_slugs.add(g["skill_slug"].lower())

        # Query database for courses targeting any of these skills
        query = (
            self.db.query(Course)
            .join(CourseSkill, Course.id == CourseSkill.course_id)
            .join(Skill, CourseSkill.skill_id == Skill.id)
            .filter(Skill.slug.in_(list(target_slugs)))
            .distinct()
        )

        all_courses = query.all()

        candidates = []
        seen_course_ids = set()

        for course in all_courses:
            if course.id in seen_course_ids:
                continue

            # Check if completed by slug or title
            if course.slug.lower() in completed_set or course.title.lower() in completed_set:
                continue

            # Extract course skill mappings
            target_skill_details = []
            course_skill_slugs = []

            for cs in course.course_skills:
                s = cs.skill
                if s:
                    course_skill_slugs.append(s.slug)
                    target_skill_details.append({
                        "skill_id": s.id,
                        "skill_slug": s.slug,
                        "skill_name": s.name,
                        "level_gained": cs.level_gained,
                        "is_primary": cs.is_primary
                    })

            # Calculate prerequisite skills for course based on DB skill prerequisites
            course_prereqs = []
            for ts_detail in target_skill_details:
                s_slug = ts_detail["skill_slug"]
                skill_obj = self.db.query(Skill).filter_by(slug=s_slug).first()
                if skill_obj and skill_obj.prerequisites:
                    for sp in skill_obj.prerequisites:
                        if sp.prerequisite_skill:
                            course_prereqs.append(sp.prerequisite_skill.slug)

            seen_course_ids.add(course.id)

            candidates.append({
                "id": course.id,
                "slug": course.slug,
                "title": course.title,
                "description": course.description,
                "provider": course.provider,
                "resource_type": course.resource_type,
                "learning_format": course.learning_format,
                "is_project_based": course.is_project_based,
                "duration_hours": course.duration_hours,
                "difficulty_level": course.difficulty_level,
                "rating": course.rating,
                "target_skills": target_skill_details,
                "skill_slugs": course_skill_slugs,
                "prerequisites": list(set(course_prereqs))
            })

        if not candidates:
            # Fallback: if no candidates matched target skills, return top available non-completed courses
            fallback_courses = self.db.query(Course).all()
            for course in fallback_courses:
                if course.slug.lower() not in completed_set and course.id not in seen_course_ids:
                    target_skill_details = [
                        {
                            "skill_id": cs.skill.id,
                            "skill_slug": cs.skill.slug,
                            "skill_name": cs.skill.name,
                            "level_gained": cs.level_gained,
                            "is_primary": cs.is_primary
                        } for cs in course.course_skills if cs.skill
                    ]
                    candidates.append({
                        "id": course.id,
                        "slug": course.slug,
                        "title": course.title,
                        "description": course.description,
                        "provider": course.provider,
                        "resource_type": course.resource_type,
                        "learning_format": course.learning_format,
                        "is_project_based": course.is_project_based,
                        "duration_hours": course.duration_hours,
                        "difficulty_level": course.difficulty_level,
                        "rating": course.rating,
                        "target_skills": target_skill_details,
                        "skill_slugs": [t["skill_slug"] for t in target_skill_details],
                        "prerequisites": []
                    })

        if not candidates:
            raise NoCandidateResourcesError("No valid candidate learning resources could be retrieved from database.")

        return candidates
