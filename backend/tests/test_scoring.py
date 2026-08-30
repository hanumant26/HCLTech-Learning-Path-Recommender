"""
Unit tests for Deterministic Scoring Engine.
Verifies score determinism, range normalization (0-100), sub-factor scoring, and explainable breakdowns.
"""
import pytest
from backend.app.services.scoring import ScoringEngine, SkillOverlapSimilarityEngine


def test_scoring_determinism():
    engine = ScoringEngine()

    candidate = {
        "id": 1,
        "slug": "python-foundations",
        "title": "Python Foundations",
        "provider": "Coursera",
        "resource_type": "course",
        "difficulty_level": "beginner",
        "duration_hours": 10.0,
        "rating": 4.8,
        "target_skills": [{"skill_slug": "python", "level_gained": 3}],
        "skill_slugs": ["python"],
        "prerequisites": []
    }

    gap_report = {
        "skill_gaps": [
            {"skill_slug": "python", "gap": 2, "importance": "critical"},
            {"skill_slug": "sql", "gap": 1, "importance": "high"}
        ]
    }

    prereq_eval = {"readiness_score": 1.0, "status": "ready", "missing_prerequisites": []}

    score_1 = engine.score_candidate(
        candidate=candidate,
        gap_report=gap_report,
        prereq_evaluation=prereq_eval,
        weekly_hours=10,
        career_skill_slugs=["python", "sql"],
        current_skills={"python": 1}
    )

    score_2 = engine.score_candidate(
        candidate=candidate,
        gap_report=gap_report,
        prereq_evaluation=prereq_eval,
        weekly_hours=10,
        career_skill_slugs=["python", "sql"],
        current_skills={"python": 1}
    )

    assert score_1["score"] == score_2["score"]
    assert score_1["breakdown"] == score_2["breakdown"]
    assert score_1["reason_codes"] == score_2["reason_codes"]


def test_score_range_normalization():
    engine = ScoringEngine()

    candidate = {
        "id": 2,
        "slug": "sample-course",
        "title": "Sample Course",
        "provider": "edX",
        "resource_type": "course",
        "difficulty_level": "intermediate",
        "duration_hours": 5.0,
        "rating": 5.0,
        "skill_slugs": ["sql"],
        "target_skills": [{"skill_slug": "sql", "level_gained": 2}],
        "prerequisites": []
    }

    gap_report = {"skill_gaps": [{"skill_slug": "sql", "gap": 3, "importance": "critical"}]}
    prereq_eval = {"readiness_score": 1.0, "status": "ready", "missing_prerequisites": []}

    res = engine.score_candidate(
        candidate=candidate,
        gap_report=gap_report,
        prereq_evaluation=prereq_eval,
        weekly_hours=10,
        career_skill_slugs=["sql"],
        current_skills={"sql": 0}
    )

    assert 0.0 <= res["score"] <= 100.0


def test_semantic_similarity_interface():
    engine = SkillOverlapSimilarityEngine()
    sim = engine.calculate_similarity(["python", "pandas"], ["python", "sql"])
    assert 0.0 < sim < 1.0
    assert engine.calculate_similarity([], ["python"]) == 0.0
