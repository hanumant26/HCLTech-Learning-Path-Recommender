"""
Skill Gap Analysis Service.
Calculates skill gaps between target career requirements and current learner proficiencies.
"""
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from backend.app.models.career import Career, CareerSkill
from backend.app.models.skill import Skill
from backend.app.services.exceptions import UnknownCareerError, InvalidProfileError


class SkillGapAnalyzer:
    """Service to compute skill gaps for a target career and learner profile."""

    @staticmethod
    def classify_gap_status(gap_value: int) -> str:
        """
        Classify gap magnitude into standard status strings.
        gap = 0 -> proficient
        gap = 1 -> minor
        gap >= 2 -> critical
        """
        if gap_value <= 0:
            return "proficient"
        elif gap_value == 1:
            return "minor"
        else:
            return "critical"

    def analyze_gaps(self, target_career: str, current_skills: Dict[str, int], db: Session) -> Dict[str, Any]:
        """
        Analyze skill gaps for a learner targeting a specific career.

        :param target_career: Career slug or title (e.g., 'Data Scientist' or 'data-scientist')
        :param current_skills: Dict mapping skill name/slug to current level (1-5)
        :param db: SQLAlchemy Session connected to SQLite
        :return: Dict containing detailed skill gaps and overall summary
        """
        if not target_career or not isinstance(target_career, str):
            raise InvalidProfileError("Target career must be a non-empty string.")

        # Find career by slug or title (case-insensitive)
        career_obj = db.query(Career).filter(
            (Career.slug == target_career.lower().strip()) |
            (Career.title.ilike(target_career.strip()))
        ).first()

        if not career_obj:
            raise UnknownCareerError(f"Target career '{target_career}' not found in database.")

        # Normalize current_skills keys to lower/slug for robust matching
        normalized_skills = {}
        if current_skills:
            # Query all skills to build a name/slug lookup
            all_skills = db.query(Skill).all()
            lookup = {}
            for s in all_skills:
                lookup[s.slug.lower()] = s.slug
                lookup[s.name.lower()] = s.slug

            for k, val in current_skills.items():
                k_clean = str(k).strip().lower()
                matched_slug = lookup.get(k_clean, k_clean)
                normalized_skills[matched_slug] = int(val)

        # Retrieve career skill requirements
        career_skills = db.query(CareerSkill).filter_by(career_id=career_obj.id).all()
        if not career_skills:
            raise UnknownCareerError(f"No skill requirements found for career '{career_obj.title}'.")

        detailed_gaps = []
        proficient_count = 0
        minor_count = 0
        critical_count = 0
        total_gap = 0
        total_required_level_sum = 0
        total_current_level_sum = 0

        for cs in career_skills:
            skill = cs.skill
            s_slug = skill.slug
            req_level = cs.required_level
            importance = cs.importance or "high"

            curr_level = normalized_skills.get(s_slug, 0)
            # Ensure non-negative and capped to req_level
            curr_level = max(0, curr_level)

            gap_val = max(0, req_level - curr_level)
            status = self.classify_gap_status(gap_val)

            if status == "proficient":
                proficient_count += 1
            elif status == "minor":
                minor_count += 1
            else:
                critical_count += 1

            total_gap += gap_val
            total_required_level_sum += req_level
            total_current_level_sum += min(curr_level, req_level)

            detailed_gaps.append({
                "skill_id": skill.id,
                "skill": skill.name,
                "skill_slug": skill.slug,
                "category": skill.category,
                "current_level": curr_level,
                "required_level": req_level,
                "gap": gap_val,
                "status": status,
                "importance": importance,
                "is_core": cs.is_core
            })

        total_skills = len(detailed_gaps)
        readiness_pct = (total_current_level_sum / total_required_level_sum * 100.0) if total_required_level_sum > 0 else 100.0

        summary = {
            "career_id": career_obj.id,
            "career_slug": career_obj.slug,
            "career_title": career_obj.title,
            "total_required_skills": total_skills,
            "proficient_count": proficient_count,
            "minor_gap_count": minor_count,
            "critical_gap_count": critical_count,
            "total_gap_points": total_gap,
            "readiness_percentage": round(readiness_pct, 1)
        }

        return {
            "summary": summary,
            "skill_gaps": detailed_gaps
        }
