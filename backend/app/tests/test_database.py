"""
Unit tests for database initialization, schema creation, relationship integrity, and constraint validation.
"""
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from backend.app.core.database import Base
from backend.app.models.user import User
from backend.app.models.profile import LearnerProfile, UserSkill
from backend.app.models.skill import Skill, SkillPrerequisite
from backend.app.models.career import Career, CareerSkill
from backend.app.models.course import Course, CourseSkill
from backend.app.models.learning_path import LearningPath, PathItem
from backend.app.models.progress import Progress
from backend.app.models.feedback import Feedback
from backend.app.models.assessment import Assessment, AssessmentResult

from backend.app.schemas.profile import UserSkillBase
from backend.app.schemas.career import CareerSkillBase
from backend.app.schemas.skill import SkillPrerequisiteBase


@pytest.fixture(scope="function")
def test_db_session():
    """In-memory SQLite database session fixture for isolated testing."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session, engine
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_database_initialization_and_table_creation(test_db_session):
    """Verify database initialization works and all 15 expected tables are created."""
    session, engine = test_db_session
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    expected_tables = {
        "users", "learner_profiles", "skills", "user_skills", "careers",
        "career_skills", "skill_prerequisites", "courses", "course_skills",
        "learning_paths", "path_items", "progress", "feedback",
        "assessments", "assessment_results"
    }

    assert expected_tables.issubset(set(table_names)), f"Missing tables: {expected_tables - set(table_names)}"


def test_relationships_validity(test_db_session):
    """Verify ORM relationships between User, Profile, UserSkill, Career, and LearningPath work correctly."""
    session, _ = test_db_session

    # Create User
    user = User(email="test.user@hcltech.com", name="Test User")
    session.add(user)
    session.flush()

    # Create Profile linked to User
    profile = LearnerProfile(
        user_id=user.id,
        target_role="AI Engineer",
        weekly_hours=15,
        experience_level="intermediate"
    )
    session.add(profile)
    session.flush()

    # Create Skill
    skill = Skill(slug="python", name="Python", category="Programming Language")
    session.add(skill)
    session.flush()

    # Link UserSkill
    user_skill = UserSkill(profile_id=profile.id, skill_id=skill.id, proficiency_level=3)
    session.add(user_skill)

    # Create Career & CareerSkill
    career = Career(slug="ai-engineer", title="AI Engineer")
    session.add(career)
    session.flush()
    career_skill = CareerSkill(career_id=career.id, skill_id=skill.id, required_level=4)
    session.add(career_skill)

    # Create LearningPath & PathItem
    path = LearningPath(profile_id=profile.id, career_id=career.id, title="AI Engineering Track")
    session.add(path)
    session.flush()
    path_item = PathItem(path_id=path.id, title="Intro to Python", sequence_order=1)
    session.add(path_item)

    session.commit()

    # Query back and verify ORM navigation
    fetched_user = session.query(User).filter_by(email="test.user@hcltech.com").first()
    assert fetched_user is not None
    assert fetched_user.profile.target_role == "AI Engineer"
    assert len(fetched_user.profile.skills) == 1
    assert fetched_user.profile.skills[0].skill.name == "Python"
    assert len(fetched_user.profile.learning_paths) == 1
    assert fetched_user.profile.learning_paths[0].path_items[0].title == "Intro to Python"


def test_skill_proficiency_accepts_only_values_1_to_5(test_db_session):
    """Verify that skill proficiency is enforced between 1 and 5 in schema and database."""
    session, _ = test_db_session

    # 1. Test Pydantic Schema validations
    with pytest.raises(ValidationError):
        UserSkillBase(skill_id=1, proficiency_level=0)

    with pytest.raises(ValidationError):
        UserSkillBase(skill_id=1, proficiency_level=6)

    valid_user_skill = UserSkillBase(skill_id=1, proficiency_level=3)
    assert valid_user_skill.proficiency_level == 3

    # 2. Test DB CheckConstraint enforcement
    user = User(email="prof.check@hcltech.com", name="Prof Check")
    session.add(user)
    session.flush()
    profile = LearnerProfile(user_id=user.id, target_role="Data Scientist")
    session.add(profile)
    skill = Skill(slug="sql", name="SQL", category="Programming Language")
    session.add(skill)
    session.flush()

    invalid_user_skill = UserSkill(profile_id=profile.id, skill_id=skill.id, proficiency_level=10)
    session.add(invalid_user_skill)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_career_skill_requirements_accept_levels_1_to_5(test_db_session):
    """Verify that career skill requirements accept levels 1–5 and reject invalid values."""
    session, _ = test_db_session

    # 1. Test Pydantic Schema validations
    with pytest.raises(ValidationError):
        CareerSkillBase(skill_id=1, required_level=0)

    with pytest.raises(ValidationError):
        CareerSkillBase(skill_id=1, required_level=6)

    valid_cs = CareerSkillBase(skill_id=1, required_level=5)
    assert valid_cs.required_level == 5

    # 2. Test DB CheckConstraint enforcement
    career = Career(slug="data-analyst", title="Data Analyst")
    skill = Skill(slug="excel", name="Excel", category="Tool")
    session.add_all([career, skill])
    session.flush()

    invalid_cs = CareerSkill(career_id=career.id, skill_id=skill.id, required_level=99)
    session.add(invalid_cs)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_prerequisite_relationships_insertion(test_db_session):
    """Verify that prerequisite relationships can be inserted and queried properly."""
    session, _ = test_db_session

    skill_a = Skill(slug="math-basics", name="Math Basics", category="Concept")
    skill_b = Skill(slug="calculus", name="Calculus", category="Concept")
    session.add_all([skill_a, skill_b])
    session.flush()

    prereq = SkillPrerequisite(
        skill_id=skill_b.id, # Calculus requires Math Basics
        prerequisite_skill_id=skill_a.id,
        required_level=2
    )
    session.add(prereq)
    session.commit()

    # Query Calculus and check prerequisites
    calculus_skill = session.query(Skill).filter_by(slug="calculus").first()
    assert len(calculus_skill.prerequisites) == 1
    assert calculus_skill.prerequisites[0].prerequisite_skill.name == "Math Basics"
    assert calculus_skill.prerequisites[0].required_level == 2

    # Verify Pydantic schema validation for prerequisite level
    with pytest.raises(ValidationError):
        SkillPrerequisiteBase(skill_id=skill_b.id, prerequisite_skill_id=skill_a.id, required_level=6)
