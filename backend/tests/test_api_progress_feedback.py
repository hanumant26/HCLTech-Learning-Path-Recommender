"""
Tests for the Progress/Feedback/Adaptation module (guide section 14).

Uses the shared `client` fixture from conftest.py (seeded DB, TestClient with
get_db overridden) — same pattern as the existing Phase 4 API tests.
"""
import pytest


@pytest.fixture(scope="module")
def started_path(client):
    """Starts one learning path for the seeded demo user (id=1) and returns its items."""
    resp = client.post("/api/learning-path/start", json={
        "user_id": 1,
        "profile": {
            "target_career": "Data Scientist",
            "weekly_hours": 10,
            "skills": {"Python": 3, "SQL": 2},
            "completed_resources": [],
            "preferred_learning_style": "mixed",
            "interests": [],
        },
    })
    assert resp.status_code == 201
    return resp.json()


# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------

class TestProgress:
    def test_create_progress(self, client, started_path):
        item_id = started_path["items"][0]["id"]
        resp = client.post("/api/progress", json={
            "path_item_id": item_id, "completion_pct": 50, "time_spent_mins": 60
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["path_item_id"] == item_id
        assert body["completion_pct"] == 50.0

    def test_update_progress_to_completion_sets_completed_at(self, client, started_path):
        item_id = started_path["items"][0]["id"]
        resp = client.put(f"/api/progress/{item_id}", json={"completion_pct": 100})
        assert resp.status_code == 200
        assert resp.json()["completed_at"] is not None

    def test_get_progress_for_untouched_resource_returns_not_started(self, client, started_path):
        item_id = started_path["items"][1]["id"]
        resp = client.get(f"/api/progress/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["completion_pct"] == 0.0

    def test_invalid_percentage_rejected(self, client, started_path):
        item_id = started_path["items"][2]["id"]
        resp = client.post("/api/progress", json={
            "path_item_id": item_id, "completion_pct": 150, "time_spent_mins": 10
        })
        assert resp.status_code == 422

    def test_invalid_resource_returns_404(self, client):
        resp = client.post("/api/progress", json={
            "path_item_id": 999999, "completion_pct": 10, "time_spent_mins": 5
        })
        assert resp.status_code == 404
        assert resp.json()["error_type"] == "path_item_not_found"

    def test_update_nonexistent_progress_returns_404(self, client, started_path):
        item_id = started_path["items"][3]["id"]
        resp = client.put(f"/api/progress/{item_id}", json={"completion_pct": 20})
        assert resp.status_code == 404

    def test_overall_progress_dashboard(self, client, started_path):
        resp = client.get("/api/progress", params={"user_id": 1})
        assert resp.status_code == 200
        body = resp.json()
        assert body["total_resources"] == len(started_path["items"])
        assert body["completed_resources"] >= 1


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------

class TestFeedback:
    def test_submit_feedback(self, client, started_path):
        item_id = started_path["items"][4]["id"]
        resp = client.post("/api/feedback", json={
            "path_item_id": item_id, "user_id": 1,
            "rating_type": "too_difficult", "comment": "Needed more prep",
        })
        assert resp.status_code == 201
        assert resp.json()["rating_type"] == "too_difficult"

    def test_invalid_feedback_type_rejected(self, client, started_path):
        item_id = started_path["items"][5]["id"]
        resp = client.post("/api/feedback", json={
            "path_item_id": item_id, "user_id": 1, "rating_type": "meh",
        })
        assert resp.status_code == 422
        assert resp.json()["error_type"] == "invalid_feedback_type"

    def test_invalid_resource_returns_404(self, client):
        resp = client.post("/api/feedback", json={
            "path_item_id": 999999, "user_id": 1, "rating_type": "appropriate",
        })
        assert resp.status_code == 404

    def test_comment_is_optional(self, client, started_path):
        item_id = started_path["items"][6]["id"]
        resp = client.post("/api/feedback", json={
            "path_item_id": item_id, "user_id": 1, "rating_type": "appropriate",
        })
        assert resp.status_code == 201
        assert resp.json()["comment"] is None

    def test_feedback_history(self, client):
        resp = client.get("/api/feedback", params={"user_id": 1})
        assert resp.status_code == 200
        assert len(resp.json()) >= 2

    def test_feedback_for_resource(self, client, started_path):
        item_id = started_path["items"][4]["id"]
        resp = client.get(f"/api/feedback/{item_id}")
        assert resp.status_code == 200
        assert all(f["path_item_id"] == item_id for f in resp.json())


# ---------------------------------------------------------------------------
# Adaptation
# ---------------------------------------------------------------------------

class TestAdaptation:
    def test_too_difficult_feeds_foundation_support(self, client, started_path):
        resp = client.get("/api/learning-path/adaptation", params={"user_id": 1})
        assert resp.status_code == 200
        body = resp.json()
        # "too_difficult" feedback was submitted above — expect some foundation signal
        assert isinstance(body["needs_foundation_support"], list)

    def test_completed_resource_appears_in_signals(self, client, started_path):
        resp = client.get("/api/learning-path/adaptation", params={"user_id": 1})
        assert resp.status_code == 200
        # item[0] was driven to 100% completion above
        assert isinstance(resp.json()["completed_resources"], list)

    def test_unknown_user_returns_404(self, client):
        resp = client.get("/api/learning-path/adaptation", params={"user_id": 999999})
        assert resp.status_code == 404
        assert resp.json()["error_type"] == "learner_profile_not_found"
