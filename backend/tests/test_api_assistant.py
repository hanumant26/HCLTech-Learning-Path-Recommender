"""
API tests for Phase 5 LLM Conversational Assistant endpoints:
  - POST /api/assistant/chat
  - POST /api/assistant/explain-resource
  - GET  /api/assistant/status
"""
import pytest
from fastapi.testclient import TestClient


def test_get_assistant_status(client: TestClient):
    """GET /api/assistant/status should return engine readiness."""
    resp = client.get("/api/assistant/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert "llm_provider" in data
    assert "api_key_configured" in data


def test_chat_why_recommended(client: TestClient):
    """POST /api/assistant/chat explaining a recommended course."""
    payload = {
        "message": "Why was Python for Data Science recommended for me?",
        "profile": {
            "target_career": "Data Scientist",
            "weekly_hours": 10,
            "skills": {"Python": 1}
        },
        "resource_slug": "python-for-everybody"
    }
    resp = client.post("/api/assistant/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "why_recommended"
    assert len(data["answer"]) > 20
    assert "python-for-everybody" in data["referenced_resources"]
    assert data["engine"] in ["gemini", "deterministic-fallback"]
    assert "target_career" in data["grounding_summary"]


def test_chat_what_next(client: TestClient):
    """POST /api/assistant/chat asking for next learning steps."""
    payload = {
        "message": "What should I learn next?",
        "profile": {
            "target_career": "Data Scientist",
            "weekly_hours": 10,
            "skills": {"Python": 2, "SQL": 1}
        }
    }
    resp = client.post("/api/assistant/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "what_next"
    assert len(data["answer"]) > 20


def test_chat_skip_prerequisite(client: TestClient):
    """POST /api/assistant/chat asking about skipping prerequisites."""
    payload = {
        "message": "Can I skip the prerequisites and start with advanced ML?",
        "profile": {
            "target_career": "Machine Learning Engineer",
            "weekly_hours": 10,
            "skills": {}
        }
    }
    resp = client.post("/api/assistant/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "skip_prerequisite"


def test_chat_time_budget(client: TestClient):
    """POST /api/assistant/chat asking about limited study time."""
    payload = {
        "message": "I only have 5 hours a week, what should I focus on?",
        "profile": {
            "target_career": "Data Analyst",
            "weekly_hours": 5,
            "skills": {}
        }
    }
    resp = client.post("/api/assistant/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "time_budget"
    assert "5 Hours/Week" in data["answer"] or "5 hours" in data["answer"].lower()


def test_explain_resource_endpoint(client: TestClient):
    """POST /api/assistant/explain-resource single-click explanation."""
    payload = {
        "resource_slug": "python-for-everybody",
        "profile": {
            "target_career": "Data Scientist",
            "weekly_hours": 10,
            "skills": {}
        }
    }
    resp = client.post("/api/assistant/explain-resource", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "python-for-everybody" in data["referenced_resources"]


def test_chat_invalid_profile(client: TestClient):
    """POST /api/assistant/chat with unknown career returns 404."""
    payload = {
        "message": "What should I learn?",
        "profile": {
            "target_career": "Quantum Astronaut",
            "weekly_hours": 10,
            "skills": {}
        }
    }
    resp = client.post("/api/assistant/chat", json=payload)
    assert resp.status_code == 404
    assert resp.json()["error_type"] == "career_not_found"
