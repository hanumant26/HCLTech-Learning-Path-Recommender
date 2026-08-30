"""
Idempotent Database Seeding Mechanism for Knowledge Base Data.
Populates skills, careers, career_skills, skill_prerequisites, courses/resources, course_skills, and assessments.
Running multiple times does NOT create duplicate records.
"""
import sys
from pathlib import Path

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, init_db
from backend.app.models.skill import Skill, SkillPrerequisite
from backend.app.models.career import Career, CareerSkill
from backend.app.models.course import Course, CourseSkill
from backend.app.models.assessment import Assessment, AssessmentResult
from backend.app.models.user import User
from backend.app.models.profile import LearnerProfile, UserSkill

from backend.app.data.skills_data import SKILLS_DATA
from backend.app.data.careers_data import CAREERS_DATA, CAREER_SKILLS_DATA
from backend.app.data.prerequisites_data import PREREQUISITES_DATA
from backend.app.data.resources_data import RESOURCES_DATA
from backend.app.data.assessments_data import ASSESSMENTS_DATA


def seed_skills(db: Session) -> dict:
    """Seed skills taxonomy idempotently."""
    skill_map = {}
    for s_data in SKILLS_DATA:
        existing = db.query(Skill).filter_by(slug=s_data["slug"]).first()
        if not existing:
            s_obj = Skill(**s_data)
            db.add(s_obj)
            db.flush()
            skill_map[s_data["slug"]] = s_obj
        else:
            # Update existing attributes if needed
            existing.name = s_data["name"]
            existing.category = s_data["category"]
            existing.description = s_data["description"]
            skill_map[s_data["slug"]] = existing
    db.commit()
    return skill_map


def seed_careers(db: Session, skill_map: dict) -> dict:
    """Seed career goals and career skill requirements idempotently."""
    career_map = {}
    for c_data in CAREERS_DATA:
        existing = db.query(Career).filter_by(slug=c_data["slug"]).first()
        if not existing:
            c_obj = Career(**c_data)
            db.add(c_obj)
            db.flush()
            career_map[c_data["slug"]] = c_obj
        else:
            existing.title = c_data["title"]
            existing.description = c_data["description"]
            career_map[c_data["slug"]] = existing

    db.commit()

    # Seed Career-to-Skill mappings
    for cs_data in CAREER_SKILLS_DATA:
        c_slug = cs_data["career_slug"]
        s_slug = cs_data["skill_slug"]
        if c_slug in career_map and s_slug in skill_map:
            c_id = career_map[c_slug].id
            s_id = skill_map[s_slug].id
            existing_cs = db.query(CareerSkill).filter_by(career_id=c_id, skill_id=s_id).first()
            if not existing_cs:
                cs_obj = CareerSkill(
                    career_id=c_id,
                    skill_id=s_id,
                    required_level=cs_data["required_level"],
                    importance=cs_data["importance"],
                    is_core=cs_data["is_core"]
                )
                db.add(cs_obj)
            else:
                existing_cs.required_level = cs_data["required_level"]
                existing_cs.importance = cs_data["importance"]
                existing_cs.is_core = cs_data["is_core"]

    db.commit()
    return career_map


def seed_prerequisites(db: Session, skill_map: dict) -> None:
    """Seed prerequisite graph idempotently."""
    for target_slug, prereq_slug, req_level in PREREQUISITES_DATA:
        if target_slug in skill_map and prereq_slug in skill_map:
            s_id = skill_map[target_slug].id
            p_id = skill_map[prereq_slug].id
            existing = db.query(SkillPrerequisite).filter_by(skill_id=s_id, prerequisite_skill_id=p_id).first()
            if not existing:
                prereq_obj = SkillPrerequisite(
                    skill_id=s_id,
                    prerequisite_skill_id=p_id,
                    required_level=req_level
                )
                db.add(prereq_obj)
            else:
                existing.required_level = req_level
    db.commit()


def seed_resources(db: Session, skill_map: dict) -> None:
    """Seed learning resources catalog and resource-to-skill mappings idempotently."""
    for r_data in RESOURCES_DATA:
        slug = r_data["slug"]
        existing = db.query(Course).filter_by(slug=slug).first()

        course_kwargs = {
            "slug": slug,
            "title": r_data["title"],
            "description": r_data.get("description"),
            "provider": r_data["provider"],
            "url": r_data.get("url") if r_data.get("url") else None,
            "resource_type": r_data["resource_type"],
            "learning_format": r_data.get("learning_format", "interactive"),
            "is_project_based": r_data.get("is_project_based", False),
            "duration_hours": r_data["duration_hours"],
            "difficulty_level": r_data["difficulty_level"],
            "rating": r_data.get("rating")
        }

        if not existing:
            c_obj = Course(**course_kwargs)
            db.add(c_obj)
            db.flush()
            course_id = c_obj.id
        else:
            for k, v in course_kwargs.items():
                setattr(existing, k, v)
            db.flush()
            course_id = existing.id

        # Seed target skills for resource
        for s_slug, level_gained, is_primary in r_data.get("target_skills", []):
            if s_slug in skill_map:
                s_id = skill_map[s_slug].id
                existing_cs = db.query(CourseSkill).filter_by(course_id=course_id, skill_id=s_id).first()
                if not existing_cs:
                    db.add(CourseSkill(
                        course_id=course_id,
                        skill_id=s_id,
                        level_gained=level_gained,
                        is_primary=is_primary
                    ))
                else:
                    existing_cs.level_gained = level_gained
                    existing_cs.is_primary = is_primary

    db.commit()


def seed_assessments(db: Session, skill_map: dict) -> None:
    """Seed diagnostic skill assessments idempotently."""
    for asm_data in ASSESSMENTS_DATA:
        s_slug = asm_data["skill_slug"]
        if s_slug in skill_map:
            s_id = skill_map[s_slug].id
            title = asm_data["title"]
            existing = db.query(Assessment).filter_by(skill_id=s_id, title=title).first()

            if not existing:
                a_obj = Assessment(
                    skill_id=s_id,
                    title=title,
                    description=asm_data.get("description"),
                    passing_score_pct=asm_data.get("passing_score_pct", 70.0),
                    questions=asm_data.get("questions")
                )
                db.add(a_obj)
            else:
                existing.description = asm_data.get("description")
                existing.passing_score_pct = asm_data.get("passing_score_pct", 70.0)
                existing.questions = asm_data.get("questions")

    db.commit()


def seed_demo_user(db: Session, skill_map: dict) -> None:
    """Seed local demo learner profile for testing."""
    demo_user = db.query(User).filter_by(email="demo.learner@hcltech.com").first()
    if not demo_user:
        demo_user = User(email="demo.learner@hcltech.com", name="Demo Learner", is_active=True)
        db.add(demo_user)
        db.flush()

        demo_profile = LearnerProfile(
            user_id=demo_user.id,
            target_role="AI Engineer",
            weekly_hours=12,
            experience_level="intermediate",
            preferred_learning_style="mixed"
        )
        db.add(demo_profile)
        db.flush()

        if "python" in skill_map:
            db.add(UserSkill(profile_id=demo_profile.id, skill_id=skill_map["python"].id, proficiency_level=3))
        if "sql" in skill_map:
            db.add(UserSkill(profile_id=demo_profile.id, skill_id=skill_map["sql"].id, proficiency_level=2))

    db.commit()


def seed_foundational_data(db: Session) -> None:
    """Execute complete idempotent knowledge base seeding."""
    print("=== Seeding Knowledge Base into Database ===")
    skill_map = seed_skills(db)
    print(f"[OK] Seeded {len(skill_map)} canonical skills.")

    career_map = seed_careers(db, skill_map)
    print(f"[OK] Seeded {len(career_map)} career paths & career-skill requirements.")

    seed_prerequisites(db, skill_map)
    print("[OK] Seeded prerequisite DAG connections.")

    seed_resources(db, skill_map)
    print("[OK] Seeded learning resource catalog & course-skill mappings.")

    seed_assessments(db, skill_map)
    print("[OK] Seeded diagnostic skill assessments.")

    seed_demo_user(db, skill_map)
    print("[OK] Seeded demo learner profile.")

    print("=== Database Seeding Completed Successfully ===")


if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        seed_foundational_data(db)
    finally:
        db.close()
