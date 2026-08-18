"""
End-to-end integration tests for Core Recommendation Engine.
Verifies end-to-end pipeline execution, scenario behaviors, edge cases, and deterministic output.
"""
import pytest
from backend.app.core.database import SessionLocal, init_db
from backend.app.seed_data import seed_foundational_data
from backend.app.services.recommendation_engine import RecommendationEngine
from backend.app.services.exceptions import InvalidProfileError, UnknownCareerError


@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    seed_foundational_data(db)
    yield db
    db.close()


def test_scenario_1_data_scientist(db_session):
    engine = RecommendationEngine()
    profile = {
        "target_career": "Data Scientist",
        "weekly_hours": 8,
        "skills": {
            "Python": 3,
            "SQL": 2,
            "Statistics": 1,
            "Pandas": 0,
            "Machine Learning": 0
        },
        "completed_resources": []
    }
    result = engine.generate_recommendations(profile, db_session)

    assert result["target_career"] == "Data Scientist"
    assert result["weekly_hours"] == 8
    assert len(result["recommendations"]) > 0
    assert result["learning_path"]["total_estimated_hours"] > 0
    assert result["learning_path"]["total_estimated_weeks"] > 0


def test_scenario_2_ai_engineer_skips_beginner_python(db_session):
    engine = RecommendationEngine()
    profile = {
        "target_career": "AI Engineer",
        "weekly_hours": 12,
        "skills": {
            "Python": 4,
            "Machine Learning": 3,
            "Deep Learning": 1
        },
        "completed_resources": []
    }
    result = engine.generate_recommendations(profile, db_session)

    # Beginner Python courses should not be top recommendation for Python 4
    top_titles = [r["title"].lower() for r in result["recommendations"][:3]]
    for title in top_titles:
        assert "beginner python" not in title and "python 101" not in title


def test_scenario_3_full_stack_developer(db_session):
    engine = RecommendationEngine()
    profile = {
        "target_career": "Full Stack Developer",
        "weekly_hours": 10,
        "skills": {
            "HTML/CSS": 4,
            "JavaScript": 3,
            "React": 0,
            "Node.js": 0
        },
        "completed_resources": []
    }
    result = engine.generate_recommendations(profile, db_session)

    gaps = {g["skill_slug"]: g for g in result["skill_gap_report"]["skill_gaps"]}
    assert gaps.get("react", {}).get("gap") > 0
    assert gaps.get("nodejs", {}).get("gap") > 0
    assert len(result["recommendations"]) > 0


def test_scenario_4_expert_learner(db_session):
    engine = RecommendationEngine()
    profile = {
        "target_career": "Data Scientist",
        "weekly_hours": 15,
        "skills": {
            "Python": 5,
            "SQL": 4,
            "Statistics": 4,
            "Pandas": 5,
            "Machine Learning": 4,
            "Deep Learning": 4
        },
        "completed_resources": []
    }
    result = engine.generate_recommendations(profile, db_session)
    assert result["skill_gap_report"]["summary"]["proficient_count"] >= 3


def test_deterministic_output(db_session):
    engine = RecommendationEngine()
    profile = {
        "target_career": "AI Engineer",
        "weekly_hours": 10,
        "skills": {"Python": 3},
        "completed_resources": []
    }

    res_1 = engine.generate_recommendations(profile, db_session)
    res_2 = engine.generate_recommendations(profile, db_session)

    scores_1 = [r["score"] for r in res_1["recommendations"]]
    scores_2 = [r["score"] for r in res_2["recommendations"]]
    assert scores_1 == scores_2


def test_error_handling_empty_and_invalid(db_session):
    engine = RecommendationEngine()

    with pytest.raises(InvalidProfileError):
        engine.generate_recommendations({"target_career": ""}, db_session)

    with pytest.raises(UnknownCareerError):
        engine.generate_recommendations({"target_career": "Astronaut"}, db_session)

    with pytest.raises(InvalidProfileError):
        engine.generate_recommendations({"target_career": "Data Scientist", "weekly_hours": 0}, db_session)

    with pytest.raises(InvalidProfileError):
        engine.generate_recommendations({"target_career": "Data Scientist", "skills": {"Python": 10}}, db_session)


# ---------------------------------------------------------------------------
# Regression tests — Phase 3 bug: blocked resources must not be actionable
# ---------------------------------------------------------------------------

def _make_rec(title: str, slug: str, missing_prereqs: list, **kwargs) -> dict:
    """Helper to build a minimal recommendation dict for LearningPathGenerator."""
    return {
        "resource_id": kwargs.get("resource_id", 1),
        "slug": slug,
        "title": title,
        "provider": "Test",
        "resource_type": kwargs.get("resource_type", "course"),
        "difficulty_level": kwargs.get("difficulty_level", "intermediate"),
        "duration_hours": kwargs.get("duration_hours", 10.0),
        "score": kwargs.get("score", 70),
        "readiness_status": "partially_ready" if missing_prereqs else "ready",
        "missing_prerequisites": missing_prereqs,
        "target_skills": [],
        "reason_codes": [],
        "is_project_based": False,
    }


def test_blocked_resource_not_in_actionable_sequence():
    """
    A resource with missing prerequisites must NOT appear in the roadmap sequence.
    Regression test for Phase 3 bug.
    """
    from backend.app.services.learning_path_generator import LearningPathGenerator

    missing = [{"skill_slug": "llm", "skill_name": "Large Language Models",
                "required_level": 2, "current_level": 0, "gap": 2}]
    recommendations = [
        _make_rec("RAG / LangChain", "rag-langchain", missing_prereqs=missing, resource_id=2),
        _make_rec("Large Language Models", "llm", missing_prereqs=[], resource_id=1,
                  difficulty_level="beginner"),
    ]

    gen = LearningPathGenerator()
    roadmap = gen.generate_roadmap(recommendations, gap_report={}, weekly_hours=10)

    sequence_slugs = [item["slug"] for item in roadmap["sequence"]]
    locked_slugs = [item["slug"] for item in roadmap.get("locked_items", [])]

    assert "rag-langchain" not in sequence_slugs, (
        "Resource with unmet prerequisites must not be an actionable roadmap step"
    )
    assert "rag-langchain" in locked_slugs, (
        "Resource with unmet prerequisites must appear in locked_items"
    )
    assert "llm" in sequence_slugs, (
        "Prerequisite resource (no missing prereqs) must appear as an actionable step"
    )


def test_all_prereqs_satisfied_resource_is_actionable():
    """
    A resource whose prerequisites are fully satisfied must appear as an actionable step,
    not in locked_items.
    Regression test for Phase 3 bug.
    """
    from backend.app.services.learning_path_generator import LearningPathGenerator

    recommendations = [
        _make_rec("Deep Learning Advanced", "deep-learning", missing_prereqs=[], resource_id=3,
                  difficulty_level="advanced"),
    ]

    gen = LearningPathGenerator()
    roadmap = gen.generate_roadmap(recommendations, gap_report={}, weekly_hours=10)

    sequence_slugs = [item["slug"] for item in roadmap["sequence"]]
    locked_slugs = [item["slug"] for item in roadmap.get("locked_items", [])]

    assert "deep-learning" in sequence_slugs, (
        "Resource with all prerequisites satisfied must be an actionable roadmap step"
    )
    assert "deep-learning" not in locked_slugs, (
        "Resource with all prerequisites satisfied must NOT appear in locked_items"
    )
