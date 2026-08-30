"""
Unit tests for Personalized Learning Path Generator.
Verifies phase adaptation, weekly time budget calculations, and sequence order.
"""
import pytest
from backend.app.services.learning_path_generator import LearningPathGenerator


def test_weekly_time_budget():
    generator = LearningPathGenerator()
    recs = [
        {"resource_id": 1, "slug": "c1", "title": "Course 1", "duration_hours": 10.0, "readiness_status": "ready", "difficulty_level": "intermediate"},
        {"resource_id": 2, "slug": "c2", "title": "Course 2", "duration_hours": 14.0, "readiness_status": "ready", "difficulty_level": "intermediate"}
    ]
    roadmap = generator.generate_roadmap(recs, gap_report={"skill_gaps": []}, weekly_hours=8)

    assert roadmap["total_estimated_hours"] == 24.0
    assert roadmap["total_estimated_weeks"] == 3.0  # 24 / 8 = 3.0
    assert roadmap["weekly_hours"] == 8


def test_adaptive_phase_skipping():
    generator = LearningPathGenerator()
    # All intermediate ready courses (no beginner/blocked foundations)
    recs = [
        {"resource_id": 1, "slug": "c1", "title": "Intermediate Core", "duration_hours": 10.0, "readiness_status": "ready", "difficulty_level": "intermediate"},
    ]
    roadmap = generator.generate_roadmap(recs, gap_report={"skill_gaps": []}, weekly_hours=10)

    # Should start with Phase 1 -- Core Skills if no foundations exist
    assert len(roadmap["phases"]) > 0
    first_phase = roadmap["phases"][0]
    assert "Core Skills" in first_phase["phase_name"]
