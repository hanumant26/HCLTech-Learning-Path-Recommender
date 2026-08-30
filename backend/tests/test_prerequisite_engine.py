"""
Unit tests for Prerequisite Engine Service.
Verifies NetworkX DAG resolution, prerequisite checking, missing prerequisite identification, and blocked resource tagging.
"""
import pytest
from backend.app.core.database import SessionLocal, init_db
from backend.app.seed_data import seed_foundational_data
from backend.app.services.prerequisite_engine import PrerequisiteEngine


@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    seed_foundational_data(db)
    yield db
    db.close()


def test_prerequisite_dag_loaded(db_session):
    engine = PrerequisiteEngine(db_session)
    assert engine.dag.number_of_nodes() > 0
    assert engine.dag.number_of_edges() > 0


def test_satisfied_prerequisites(db_session):
    engine = PrerequisiteEngine(db_session)
    # Learner has Python = 3, target pandas requires python
    current = {"python": 3}
    eval_res = engine.evaluate_resource_readiness(
        resource_target_skills=[("pandas", 2)],
        resource_prerequisite_skills=["python"],
        current_skills=current
    )
    assert eval_res["is_satisfied"] is True
    assert eval_res["readiness_score"] == 1.0
    assert eval_res["status"] == "ready"


def test_blocked_resource_identification(db_session):
    engine = PrerequisiteEngine(db_session)
    # Learner has Python = 0, target pandas requires python
    current = {"python": 0}
    eval_res = engine.evaluate_resource_readiness(
        resource_target_skills=[("pandas", 2)],
        resource_prerequisite_skills=["python"],
        current_skills=current
    )
    assert eval_res["is_satisfied"] is False
    assert eval_res["status"] == "blocked"
    assert len(eval_res["missing_prerequisites"]) > 0
    missing_slugs = [m["skill_slug"] for m in eval_res["missing_prerequisites"]]
    assert "python" in missing_slugs


def test_prerequisite_chain_retrieval(db_session):
    engine = PrerequisiteEngine(db_session)
    chain = engine.get_prerequisite_chain("pandas")
    assert isinstance(chain, list)
