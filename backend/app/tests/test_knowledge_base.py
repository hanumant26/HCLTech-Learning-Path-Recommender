"""
Unit tests for Knowledge Base dataset seeding, relationships, DAG validity, and data validation rules.
"""
import pytest
import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.database import Base
from backend.app.models.skill import Skill, SkillPrerequisite
from backend.app.models.career import Career, CareerSkill
from backend.app.models.course import Course, CourseSkill
from backend.app.models.assessment import Assessment
from backend.app.data.skills_data import SKILLS_DATA
from backend.app.data.careers_data import CAREERS_DATA, CAREER_SKILLS_DATA
from backend.app.data.prerequisites_data import PREREQUISITES_DATA
from backend.app.data.resources_data import RESOURCES_DATA
from backend.app.data.assessments_data import ASSESSMENTS_DATA
from backend.app.seed_data import seed_foundational_data
from backend.app.data_validator import validate_knowledge_base


@pytest.fixture(scope="function")
def kb_db_session():
    """In-memory SQLite database session fixture for isolated Knowledge Base testing."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_knowledge_base_data_validation_rules():
    """Verify that all 12 data validation rules pass on the raw dataset files."""
    assert validate_knowledge_base() is True


def test_prerequisite_graph_is_dag():
    """Verify that the skill prerequisite graph forms a valid Directed Acyclic Graph (DAG)."""
    dag = nx.DiGraph()
    skill_slugs = {s["slug"] for s in SKILLS_DATA}
    for s_slug in skill_slugs:
        dag.add_node(s_slug)

    for target_slug, prereq_slug, _ in PREREQUISITES_DATA:
        assert target_slug in skill_slugs, f"Target skill '{target_slug}' missing from SKILLS_DATA"
        assert prereq_slug in skill_slugs, f"Prerequisite skill '{prereq_slug}' missing from SKILLS_DATA"
        dag.add_edge(prereq_slug, target_slug)

    assert nx.is_directed_acyclic_graph(dag) is True, "Prerequisite graph contains cycles!"


def test_skill_and_career_insertion(kb_db_session):
    """Verify skill and career dataset insertion into SQLite."""
    seed_foundational_data(kb_db_session)

    skill_count = kb_db_session.query(Skill).count()
    assert skill_count == len(SKILLS_DATA)
    assert skill_count >= 80

    career_count = kb_db_session.query(Career).count()
    assert career_count == 5

    py_skill = kb_db_session.query(Skill).filter_by(slug="python").first()
    assert py_skill is not None
    assert py_skill.category == "Programming Language"


def test_career_skill_relationships(kb_db_session):
    """Verify career-to-skill requirement mappings and importance attributes."""
    seed_foundational_data(kb_db_session)

    ai_career = kb_db_session.query(Career).filter_by(slug="ai-engineer").first()
    assert ai_career is not None
    assert len(ai_career.career_skills) > 0

    py_cs = [cs for cs in ai_career.career_skills if cs.skill.slug == "python"][0]
    assert py_cs.required_level == 4
    assert py_cs.importance == "critical"
    assert py_cs.is_core is True


def test_prerequisite_insertion(kb_db_session):
    """Verify prerequisite relationships inserted in database."""
    seed_foundational_data(kb_db_session)

    pandas_skill = kb_db_session.query(Skill).filter_by(slug="pandas").first()
    assert pandas_skill is not None
    assert len(pandas_skill.prerequisites) > 0
    assert pandas_skill.prerequisites[0].prerequisite_skill.slug == "python"


def test_course_and_course_skill_insertion(kb_db_session):
    """Verify learning resources catalog insertion and target skill mappings."""
    seed_foundational_data(kb_db_session)

    course_count = kb_db_session.query(Course).count()
    assert course_count >= 150

    fastapi_course = kb_db_session.query(Course).filter_by(slug="fastapi-web-api-bootcamp").first()
    assert fastapi_course is not None
    assert fastapi_course.resource_type == "course"
    assert len(fastapi_course.course_skills) > 0


def test_assessment_insertion(kb_db_session):
    """Verify diagnostic assessment insertion and question structure."""
    seed_foundational_data(kb_db_session)

    asm_count = kb_db_session.query(Assessment).count()
    assert asm_count == 8

    py_asm = kb_db_session.query(Assessment).filter(Assessment.title.contains("Python")).first()
    assert py_asm is not None
    assert py_asm.questions is not None
    assert len(py_asm.questions) == 5
    assert py_asm.questions[0]["correct_answer"] in py_asm.questions[0]["options"]


def test_duplicate_seed_prevention_idempotency(kb_db_session):
    """Verify that executing seed_foundational_data multiple times produces zero duplicates."""
    seed_foundational_data(kb_db_session)
    count_run1 = kb_db_session.query(Skill).count()
    course_count_run1 = kb_db_session.query(Course).count()

    # Re-run seed on same session
    seed_foundational_data(kb_db_session)
    count_run2 = kb_db_session.query(Skill).count()
    course_count_run2 = kb_db_session.query(Course).count()

    assert count_run1 == count_run2
    assert course_count_run1 == course_count_run2
