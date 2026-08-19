"""
API tests for POST /api/learner/profile (transient validation, no DB writes).
Verifies validation success, field normalization, and error HTTP codes.
"""
import pytest


VALID_PROFILE = {
    "target_career": "Data Scientist",
    "weekly_hours": 10,
    "skills": {"Python": 3, "SQL": 2},
    "completed_resources": [],
    "preferred_learning_style": "mixed",
    "interests": [],
}


def test_valid_profile_returns_200(client):
    """A well-formed profile must return HTTP 200 with valid=True."""
    response = client.post("/api/learner/profile", json=VALID_PROFILE)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True


def test_valid_profile_response_schema(client):
    """Response must contain valid, normalized_profile, and message fields."""
    response = client.post("/api/learner/profile", json=VALID_PROFILE)
    data = response.json()

    assert "valid" in data
    assert "normalized_profile" in data
    assert "message" in data
    assert isinstance(data["normalized_profile"], dict)


def test_normalized_profile_contains_expected_keys(client):
    """normalized_profile must include target_career, weekly_hours, skills."""
    response = client.post("/api/learner/profile", json=VALID_PROFILE)
    normalized = response.json()["normalized_profile"]

    assert "target_career" in normalized
    assert "weekly_hours" in normalized
    assert "skills" in normalized
    assert normalized["target_career"] == "Data Scientist"
    assert normalized["weekly_hours"] == 10


def test_empty_target_career_returns_422(client):
    """An empty target_career must return HTTP 422 (invalid_profile)."""
    payload = {**VALID_PROFILE, "target_career": ""}
    response = client.post("/api/learner/profile", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_missing_target_career_returns_422(client):
    """A request body missing target_career must return HTTP 422."""
    payload = {"weekly_hours": 10, "skills": {"Python": 3}}
    response = client.post("/api/learner/profile", json=payload)
    assert response.status_code == 422


def test_unknown_career_returns_404(client):
    """An unknown target_career must return HTTP 404 (career_not_found)."""
    payload = {**VALID_PROFILE, "target_career": "AstronautXYZ999"}
    response = client.post("/api/learner/profile", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data.get("error_type") == "career_not_found"


def test_invalid_weekly_hours_zero_returns_422(client):
    """weekly_hours=0 must return HTTP 422."""
    # Pydantic rejects ge=1 constraint before hitting the service
    payload = {**VALID_PROFILE, "weekly_hours": 0}
    response = client.post("/api/learner/profile", json=payload)
    assert response.status_code == 422


def test_skill_level_out_of_range_returns_422(client):
    """Proficiency level > 5 must return HTTP 422 from the service validator."""
    payload = {**VALID_PROFILE, "skills": {"Python": 10}}
    response = client.post("/api/learner/profile", json=payload)
    assert response.status_code == 422


def test_career_slug_accepted(client):
    """A lowercase slug (e.g. 'data-scientist') must also be accepted."""
    payload = {**VALID_PROFILE, "target_career": "data-scientist"}
    response = client.post("/api/learner/profile", json=payload)
    assert response.status_code == 200
    assert response.json()["valid"] is True
