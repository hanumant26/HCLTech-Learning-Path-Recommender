"""
Shared pytest fixtures for Phase 4 API tests.

Provides:
  - `test_db`: a seeded SQLAlchemy session (session-scoped)
  - `client`: a FastAPI TestClient wired to the seeded `test_db` via dependency override

The existing backend/tests/ test files do NOT use conftest fixtures — they each
create their own SessionLocal. This conftest is additive and does not interfere
with the 37 pre-existing tests.
"""
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.database import get_db, init_db, SessionLocal
from backend.app.seed_data import seed_foundational_data


@pytest.fixture(scope="session")
def test_db():
    """
    Initialise the database schema and seed foundational data once per test session.
    Idempotent seeding means running against the shared SQLite file is safe.
    """
    init_db()
    db = SessionLocal()
    seed_foundational_data(db)
    yield db
    db.close()


@pytest.fixture(scope="session")
def client(test_db):
    """
    FastAPI TestClient whose DB dependency is overridden to use the seeded test_db.
    httpx is already in requirements.txt so TestClient is available.
    """
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up the override after the session
    app.dependency_overrides.pop(get_db, None)
