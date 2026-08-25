"""
API tests for GET /api/careers.
Verifies status code, response schema, and data integrity.
"""
import pytest


def test_get_careers_returns_200(client):
    """GET /api/careers must return HTTP 200."""
    response = client.get("/api/careers")
    assert response.status_code == 200


def test_careers_response_has_required_top_level_keys(client):
    """Response must contain 'careers' list and 'total' integer."""
    response = client.get("/api/careers")
    data = response.json()

    assert "careers" in data
    assert "total" in data
    assert isinstance(data["careers"], list)
    assert isinstance(data["total"], int)


def test_careers_total_matches_list_length(client):
    """'total' must equal len('careers')."""
    response = client.get("/api/careers")
    data = response.json()

    assert data["total"] == len(data["careers"])


def test_careers_list_is_non_empty(client):
    """Seeded DB must have at least one career."""
    response = client.get("/api/careers")
    data = response.json()

    assert data["total"] > 0
    assert len(data["careers"]) > 0


def test_career_item_schema(client):
    """Each career item must have id, slug, title, required_skills_count fields."""
    response = client.get("/api/careers")
    careers = response.json()["careers"]

    for career in careers:
        assert "id" in career
        assert "slug" in career
        assert "title" in career
        assert "required_skills_count" in career
        assert isinstance(career["id"], int)
        assert isinstance(career["slug"], str)
        assert isinstance(career["title"], str)
        assert isinstance(career["required_skills_count"], int)
        assert career["required_skills_count"] >= 0


def test_career_slugs_are_unique(client):
    """No two careers should share the same slug."""
    response = client.get("/api/careers")
    careers = response.json()["careers"]
    slugs = [c["slug"] for c in careers]

    assert len(slugs) == len(set(slugs))


def test_known_careers_present(client):
    """Seeded careers (Data Scientist, AI Engineer, etc.) must appear."""
    response = client.get("/api/careers")
    titles = {c["title"] for c in response.json()["careers"]}

    assert "Data Scientist" in titles
