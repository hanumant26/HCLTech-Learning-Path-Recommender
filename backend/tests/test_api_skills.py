"""
API tests for GET /api/skills.
Verifies status code, response schema, category filtering, and data integrity.
"""
import pytest


def test_get_skills_returns_200(client):
    """GET /api/skills must return HTTP 200."""
    response = client.get("/api/skills")
    assert response.status_code == 200


def test_skills_response_has_required_top_level_keys(client):
    """Response must contain 'skills' list and 'total' integer."""
    response = client.get("/api/skills")
    data = response.json()

    assert "skills" in data
    assert "total" in data
    assert isinstance(data["skills"], list)
    assert isinstance(data["total"], int)


def test_skills_total_matches_list_length(client):
    """'total' must equal len('skills')."""
    response = client.get("/api/skills")
    data = response.json()

    assert data["total"] == len(data["skills"])


def test_skills_list_is_non_empty(client):
    """Seeded DB must have at least one skill."""
    response = client.get("/api/skills")
    data = response.json()

    assert data["total"] > 0


def test_skill_item_schema(client):
    """Each skill item must have id, slug, name, category fields."""
    response = client.get("/api/skills")
    skills = response.json()["skills"]

    for skill in skills:
        assert "id" in skill
        assert "slug" in skill
        assert "name" in skill
        assert "category" in skill
        assert isinstance(skill["id"], int)
        assert isinstance(skill["slug"], str)
        assert isinstance(skill["name"], str)
        assert isinstance(skill["category"], str)


def test_skill_slugs_are_unique(client):
    """No two skills should share the same slug."""
    response = client.get("/api/skills")
    skills = response.json()["skills"]
    slugs = [s["slug"] for s in skills]

    assert len(slugs) == len(set(slugs))


def test_skills_category_filter_returns_subset(client):
    """?category= filter must return only matching skills (fewer or equal to total)."""
    total_response = client.get("/api/skills")
    total = total_response.json()["total"]

    filtered_response = client.get("/api/skills?category=Programming Language")
    assert filtered_response.status_code == 200
    filtered_total = filtered_response.json()["total"]

    # Filtered result cannot exceed the unfiltered total
    assert filtered_total <= total


def test_skills_category_filter_all_items_match(client):
    """All returned skills must match the requested category (case-insensitive partial match)."""
    response = client.get("/api/skills?category=Framework")
    assert response.status_code == 200
    skills = response.json()["skills"]

    for skill in skills:
        assert "framework" in skill["category"].lower()


def test_known_skill_python_present(client):
    """'Python' must be present in the seeded skill list."""
    response = client.get("/api/skills")
    names = {s["name"] for s in response.json()["skills"]}
    assert "Python" in names
