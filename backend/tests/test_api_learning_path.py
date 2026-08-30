"""
API tests for POST /api/learning-path.
Verifies response schema, roadmap phases, sequence, weekly estimates, and error codes.
"""
import pytest


VALID_PROFILE = {
    "target_career": "Data Scientist",
    "weekly_hours": 10,
    "skills": {"Python": 3, "SQL": 2},
    "completed_resources": [],
}


def test_learning_path_returns_200(client):
    """POST /api/learning-path must return HTTP 200."""
    response = client.post("/api/learning-path", json=VALID_PROFILE)
    assert response.status_code == 200


def test_learning_path_response_has_required_keys(client):
    """Response must contain phases, sequence, total_items, total_estimated_hours, total_estimated_weeks, weekly_hours."""
    response = client.post("/api/learning-path", json=VALID_PROFILE)
    data = response.json()

    required_keys = [
        "phases",
        "sequence",
        "total_items",
        "total_estimated_hours",
        "total_estimated_weeks",
        "weekly_hours",
        "locked_items",
    ]
    for key in required_keys:
        assert key in data, f"Missing required key: '{key}'"


def test_learning_path_returns_only_learning_path_portion(client):
    """Ensure response returns only learning path roadmap without outer recommendations object."""
    response = client.post("/api/learning-path", json=VALID_PROFILE)
    data = response.json()

    assert "recommendations" not in data
    assert "skill_gap_report" not in data
    assert "target_career" not in data
    assert isinstance(data["phases"], list)
    assert isinstance(data["sequence"], list)


def test_learning_path_phases_structure(client):
    """Each phase must contain phase_number, phase_name, items, phase_hours."""
    response = client.post("/api/learning-path", json=VALID_PROFILE)
    phases = response.json()["phases"]

    assert len(phases) > 0
    for phase in phases:
        assert "phase_number" in phase
        assert "phase_name" in phase
        assert "items" in phase
        assert "phase_hours" in phase
        assert isinstance(phase["items"], list)
        assert phase["phase_hours"] >= 0


def test_learning_path_sequence_order(client):
    """Sequence items must be numbered in sequential order starting from 1."""
    response = client.post("/api/learning-path", json=VALID_PROFILE)
    sequence = response.json()["sequence"]

    if sequence:
        orders = [item["sequence_order"] for item in sequence]
        assert orders == list(range(1, len(sequence) + 1))


def test_learning_path_weekly_hours_matches_input(client):
    """weekly_hours in learning-path response must match request input."""
    response = client.post("/api/learning-path", json=VALID_PROFILE)
    data = response.json()
    assert data["weekly_hours"] == VALID_PROFILE["weekly_hours"]


def test_learning_path_top_n_param(client):
    """top_n parameter limits total items in learning path."""
    response = client.post("/api/learning-path?top_n=2", json=VALID_PROFILE)
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] <= 2


def test_learning_path_unknown_career_returns_404(client):
    """Unknown career must return HTTP 404."""
    payload = {**VALID_PROFILE, "target_career": "NonExistentCareerXYZ"}
    response = client.post("/api/learning-path", json=payload)
    assert response.status_code == 404
    assert response.json().get("error_type") == "career_not_found"


def test_learning_path_invalid_profile_returns_422(client):
    """Invalid profile (e.g. empty target_career) must return HTTP 422."""
    payload = {**VALID_PROFILE, "target_career": ""}
    response = client.post("/api/learning-path", json=payload)
    assert response.status_code == 422
