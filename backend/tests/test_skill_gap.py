"""
Unit tests for Skill Gap Analysis Service.
Verifies gap calculation, missing skill defaulting to 0, status classification, and DB requirement retrieval.
"""
import pytest
from backend.app.core.database import SessionLocal, init_db
from backend.app.seed_data import seed_foundational_data
from backend.app.services.skill_gap import SkillGapAnalyzer
from backend.app.services.exceptions import UnknownCareerError, InvalidProfileError


@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    seed_foundational_data(db)
    yield db
    db.close()


def test_missing_skills_default_to_zero(db_session):
    analyzer = SkillGapAnalyzer()
    profile_skills = {"Python": 3}  # Statistics, Pandas, ML omitted

    result = analyzer.analyze_gaps("Data Scientist", profile_skills, db_session)
    gaps = {g["skill"]: g for g in result["skill_gaps"]}

    # Missing skill in profile should have current_level = 0
    assert "Statistics" in gaps or "Descriptive Statistics" in gaps or "NumPy" in gaps
    for s_name, g in gaps.items():
        if s_name not in ["Python"]:
            assert g["current_level"] == 0
            assert g["gap"] == g["required_level"]


def test_gap_calculation_correctness(db_session):
    analyzer = SkillGapAnalyzer()
    profile_skills = {
        "Python": 3,
        "SQL": 2,
        "Statistics": 1
    }

    result = analyzer.analyze_gaps("Data Scientist", profile_skills, db_session)
    gaps = {g["skill_slug"]: g for g in result["skill_gaps"]}

    # Python: req 4, curr 3 => gap 1
    if "python" in gaps:
        assert gaps["python"]["gap"] == max(0, gaps["python"]["required_level"] - 3)

    # SQL: req 4, curr 2 => gap 2
    if "sql" in gaps:
        assert gaps["sql"]["gap"] == max(0, gaps["sql"]["required_level"] - 2)


def test_status_classification(db_session):
    analyzer = SkillGapAnalyzer()
    assert analyzer.classify_gap_status(0) == "proficient"
    assert analyzer.classify_gap_status(1) == "minor"
    assert analyzer.classify_gap_status(2) == "critical"
    assert analyzer.classify_gap_status(4) == "critical"


def test_unknown_career_raises_error(db_session):
    analyzer = SkillGapAnalyzer()
    with pytest.raises(UnknownCareerError):
        analyzer.analyze_gaps("NonExistentCareerXYZ", {}, db_session)


def test_invalid_profile_raises_error(db_session):
    analyzer = SkillGapAnalyzer()
    with pytest.raises(InvalidProfileError):
        analyzer.analyze_gaps("", {}, db_session)
