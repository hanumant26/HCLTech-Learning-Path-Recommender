"""
Unit tests for Candidate Resource Retrieval Service.
Verifies DB queries, target skill filtering, and completed resource exclusion.
"""
import pytest
from backend.app.core.database import SessionLocal, init_db
from backend.app.seed_data import seed_foundational_data
from backend.app.services.candidate_retriever import CandidateRetriever
from backend.app.models.course import Course


@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    seed_foundational_data(db)
    yield db
    db.close()


def test_candidate_retrieval_success(db_session):
    retriever = CandidateRetriever(db_session)
    gap_skills = [{"skill_slug": "python", "gap": 2}, {"skill_slug": "sql", "gap": 1}]

    candidates = retriever.retrieve_candidates(
        gap_skills=gap_skills,
        prerequisite_missing_skills=[],
        completed_resources=[]
    )

    assert len(candidates) > 0
    for c in candidates:
        assert "slug" in c
        assert "title" in c
        assert "target_skills" in c


def test_completed_resources_excluded(db_session):
    retriever = CandidateRetriever(db_session)
    # Find a course slug in DB
    sample_course = db_session.query(Course).first()
    completed_slug = sample_course.slug

    gap_skills = [{"skill_slug": "python", "gap": 3}]
    candidates = retriever.retrieve_candidates(
        gap_skills=gap_skills,
        prerequisite_missing_skills=[],
        completed_resources=[completed_slug]
    )

    retrieved_slugs = [c["slug"] for c in candidates]
    assert completed_slug not in retrieved_slugs
