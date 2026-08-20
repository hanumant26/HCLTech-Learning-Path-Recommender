"""
Unit tests for ConversationalAssistantService (Phase 5).
"""
import pytest
from backend.app.core.database import SessionLocal, init_db
from backend.app.seed_data import seed_foundational_data
from backend.app.services.assistant_service import ConversationalAssistantService
from backend.app.schemas.assistant import ChatMessage


@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    seed_foundational_data(db)
    yield db
    db.close()


@pytest.fixture(scope="module")
def assistant_service():
    return ConversationalAssistantService()


def test_intent_classification(assistant_service):
    """Verify that user queries correctly classify into supported intent categories."""
    assert assistant_service.classify_intent("Why was Machine Learning Specialization recommended to me?") == "why_recommended"
    assert assistant_service.classify_intent("Why is Deep Learning with PyTorch locked?") == "why_locked"
    assert assistant_service.classify_intent("What should I learn next?") == "what_next"
    assert assistant_service.classify_intent("Where do I start?") == "what_next"
    assert assistant_service.classify_intent("Can I skip Python for Data Science and jump directly?") == "skip_prerequisite"
    assert assistant_service.classify_intent("I only have 5 hours per week, what should I focus on?") == "time_budget"
    assert assistant_service.classify_intent("How can I prepare for AI Engineer role?") == "general_guidance"


def test_grounding_context_builder(assistant_service, db_session):
    """Verify grounding context accurately pulls skill gaps, recommendations, and roadmap."""
    profile = {
        "target_career": "Data Scientist",
        "weekly_hours": 10,
        "skills": {"Python": 1, "SQL": 1}
    }
    context = assistant_service.build_grounding_context(profile, db=db_session)
    assert context["target_career"] == "Data Scientist"
    assert context["weekly_hours"] == 10
    assert "skill_gap_report" in context
    assert len(context["top_recommendations"]) > 0
    assert "phases" in context["learning_path"]


def test_explain_why_recommended(assistant_service, db_session):
    """Verify grounded explanation for why a resource is recommended."""
    profile = {
        "target_career": "Data Scientist",
        "weekly_hours": 10,
        "skills": {"Python": 1, "SQL": 1}
    }
    response = assistant_service.generate_chat_response(
        message="Why was Python for Everybody Specialization recommended?",
        profile_data=profile,
        db=db_session,
        resource_slug="python-for-everybody"
    )
    assert response["intent"] == "why_recommended"
    assert "Python for Everybody" in response["answer"]
    assert "Score Breakdown" in response["answer"]
    assert response["engine"] in ["gemini", "deterministic-fallback"]
    assert response["grounding_summary"]["target_career"] == "Data Scientist"


def test_explain_why_locked(assistant_service, db_session):
    """Verify grounded explanation for locked courses and missing prerequisites."""
    # Learner with no Python proficiency attempting ML Engineer
    profile = {
        "target_career": "Machine Learning Engineer",
        "weekly_hours": 10,
        "skills": {"Python": 0}
    }
    response = assistant_service.generate_chat_response(
        message="Why is this course locked?",
        profile_data=profile,
        db=db_session,
        resource_slug="machine-learning-specialization"
    )
    assert response["intent"] == "why_locked"
    assert "Locked" in response["answer"] or "Prerequisite" in response["answer"]
    assert "How to Unlock" in response["answer"] or "Prerequisite Status" in response["answer"]


def test_explain_what_next(assistant_service, db_session):
    """Verify sequential next step recommendations based on roadmap phase 1."""
    profile = {
        "target_career": "Data Scientist",
        "weekly_hours": 15,
        "skills": {"Python": 2, "SQL": 2}
    }
    response = assistant_service.generate_chat_response(
        message="What should I learn next?",
        profile_data=profile,
        db=db_session
    )
    assert response["intent"] == "what_next"
    assert "Phase 1" in response["answer"] or "Step 1" in response["answer"]
    assert "hours" in response["answer"]


def test_explain_skip_prerequisite(assistant_service, db_session):
    """Verify guidance when a learner asks about skipping prerequisites."""
    profile = {
        "target_career": "AI Engineer",
        "weekly_hours": 10,
        "skills": {}
    }
    response = assistant_service.generate_chat_response(
        message="Can I skip the introductory prerequisites?",
        profile_data=profile,
        db=db_session
    )
    assert response["intent"] == "skip_prerequisite"
    assert "advise against" in response["answer"].lower() or "prerequisite" in response["answer"].lower()


def test_explain_time_budget(assistant_service, db_session):
    """Verify time budget and pacing guidance."""
    profile = {
        "target_career": "Data Analyst",
        "weekly_hours": 5,
        "skills": {"SQL": 1}
    }
    response = assistant_service.generate_chat_response(
        message="I only have 5 hours a week, what should I focus on?",
        profile_data=profile,
        db=db_session
    )
    assert response["intent"] == "time_budget"
    assert "5 Hours/Week" in response["answer"]
    assert "Phase 1" in response["answer"] or "Focus" in response["answer"]
