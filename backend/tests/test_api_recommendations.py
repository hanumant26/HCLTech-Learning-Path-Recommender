"""
API tests for POST /api/recommendations/generate.
Verifies full pipeline execution, response schema, error codes, top_n limiting,
and embedded learning_path block.
"""
import pytest


VALID_PROFILE = {
    "target_career": "Data Scientist",
    "weekly_hours": 10,
    "skills": {"Python": 3, "SQL": 2},
    "completed_resources": [],
}


def test_generate_recommendations_returns_200(client):
    """POST /api/recommendations/generate must return HTTP 200."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    assert response.status_code == 200


def test_response_contains_required_top_level_fields(client):
    """Response must contain all required top-level keys."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    data = response.json()

    required_keys = [
        "target_career",
        "career_slug",
        "weekly_hours",
        "skill_gap_report",
        "total_candidates_found",
        "recommendations",
        "learning_path",
    ]
    for key in required_keys:
        assert key in data, f"Missing required key: '{key}'"


def test_recommendations_list_is_non_empty(client):
    """Recommendations list must contain at least one item for a valid profile."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    data = response.json()

    assert len(data["recommendations"]) > 0


def test_recommendation_item_schema(client):
    """Each recommendation item must have the required fields."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    recommendations = response.json()["recommendations"]

    required_item_keys = [
        "resource_id", "slug", "title", "provider",
        "score", "breakdown", "reason_codes",
        "readiness_status", "difficulty_level", "duration_hours",
    ]
    for item in recommendations:
        for key in required_item_keys:
            assert key in item, f"Recommendation item missing key: '{key}'"


def test_score_breakdown_fields(client):
    """Score breakdown must contain all 7 sub-factor scores."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    first_rec = response.json()["recommendations"][0]
    breakdown = first_rec["breakdown"]

    expected_factors = [
        "goal_relevance", "skill_gap", "prerequisite_readiness",
        "semantic_similarity", "difficulty_match", "time_fit", "quality",
    ]
    for factor in expected_factors:
        assert factor in breakdown, f"Breakdown missing factor: '{factor}'"


def test_scores_are_in_valid_range(client):
    """All recommendation scores must be in [0, 100]."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    for rec in response.json()["recommendations"]:
        assert 0.0 <= rec["score"] <= 100.0


def test_recommendations_ordered_by_score_descending(client):
    """Recommendations must be sorted by score descending."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    scores = [r["score"] for r in response.json()["recommendations"]]
    assert scores == sorted(scores, reverse=True)


def test_skill_gap_report_present(client):
    """skill_gap_report must have summary and skill_gaps keys."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    gap_report = response.json()["skill_gap_report"]

    assert "summary" in gap_report
    assert "skill_gaps" in gap_report
    assert isinstance(gap_report["skill_gaps"], list)


def test_learning_path_embedded_in_response(client):
    """learning_path block must be present with phases and sequence."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    lp = response.json()["learning_path"]

    assert "phases" in lp
    assert "sequence" in lp
    assert "total_items" in lp
    assert "total_estimated_hours" in lp
    assert "total_estimated_weeks" in lp
    assert "weekly_hours" in lp


def test_learning_path_hours_positive(client):
    """total_estimated_hours must be > 0 when recommendations exist."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    lp = response.json()["learning_path"]
    assert lp["total_estimated_hours"] > 0


def test_top_n_param_limits_results(client):
    """?top_n=3 must return at most 3 recommendations."""
    response = client.post("/api/recommendations/generate?top_n=3", json=VALID_PROFILE)
    assert response.status_code == 200
    recs = response.json()["recommendations"]
    assert len(recs) <= 3


def test_unknown_career_returns_404(client):
    """An unknown target_career must return HTTP 404."""
    payload = {**VALID_PROFILE, "target_career": "AstronautXYZ999"}
    response = client.post("/api/recommendations/generate", json=payload)
    assert response.status_code == 404
    assert response.json().get("error_type") == "career_not_found"


def test_invalid_profile_empty_career_returns_422(client):
    """An empty target_career must return HTTP 422."""
    payload = {**VALID_PROFILE, "target_career": ""}
    response = client.post("/api/recommendations/generate", json=payload)
    assert response.status_code == 422


def test_invalid_profile_bad_skill_level_returns_422(client):
    """A skill proficiency > 5 must return HTTP 422."""
    payload = {**VALID_PROFILE, "skills": {"Python": 99}}
    response = client.post("/api/recommendations/generate", json=payload)
    assert response.status_code == 422


def test_career_title_in_response_matches_input(client):
    """target_career in the response must match the known DB title."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    assert response.json()["target_career"] == "Data Scientist"


def test_weekly_hours_reflected_in_response(client):
    """weekly_hours in response must match the request."""
    response = client.post("/api/recommendations/generate", json=VALID_PROFILE)
    assert response.json()["weekly_hours"] == VALID_PROFILE["weekly_hours"]


def test_recommendations_generate_handles_locked_items_without_phase_fields(client):
    """
    Regression test: locked_items do not have sequence_order, phase_number, or phase_name.
    Endpoint must return HTTP 200 and serialize locked_items properly without 500 schema validation errors.
    """
    payload = {
        "target_career": "AI Engineer",
        "weekly_hours": 10,
        "skills": {},
    }
    response = client.post("/api/recommendations/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "learning_path" in data
    assert "locked_items" in data["learning_path"]
    assert isinstance(data["learning_path"]["locked_items"], list)
    for locked_item in data["learning_path"]["locked_items"]:
        assert locked_item.get("sequence_order") is None
        assert locked_item.get("phase_number") is None
        assert locked_item.get("phase_name") is None

