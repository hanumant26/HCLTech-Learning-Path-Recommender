"""
Path Persistence Service (Progress/Feedback/Adaptation module).

The existing RecommendationEngine (Phases 1-5) is stateless: it computes a
roadmap on every call but never saves it. Progress and Feedback, however,
are keyed on `path_item_id` — a real database row.

This service is a thin, additive bridge: it calls the existing
RecommendationEngine UNCHANGED and simply persists its output as
LearningPath + PathItem rows so a learner can start tracking progress on
a generated path.

Does NOT touch skill-gap analysis, prerequisite resolution, candidate
retrieval, scoring, or roadmap generation.
"""
from typing import Any, Dict
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.models.profile import LearnerProfile
from backend.app.models.career import Career
from backend.app.models.learning_path import LearningPath, PathItem
from backend.app.services.recommendation_engine import RecommendationEngine
from backend.app.services.exceptions import InvalidProfileError

_engine = RecommendationEngine()


def _get_or_create_profile(user_id: int, profile_data: Dict[str, Any], db: Session) -> LearnerProfile:
    """Reuses LearnerProfile if one exists for this user; creates it otherwise."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise InvalidProfileError(f"User with id {user_id} does not exist.")

    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user_id).first()
    if profile is None:
        profile = LearnerProfile(
            user_id=user_id,
            target_role=profile_data.get("target_career"),
            weekly_hours=profile_data.get("weekly_hours", 10),
            preferred_learning_style=profile_data.get("preferred_learning_style", "mixed"),
        )
        db.add(profile)
        db.flush()
    return profile


def start_learning_path(
    user_id: int,
    profile_data: Dict[str, Any],
    db: Session,
    top_n: int = 10,
) -> LearningPath:
    """
    Runs the existing (unmodified) recommendation pipeline and persists the
    resulting roadmap as a LearningPath with its PathItem rows.

    Any previously active path for this profile is archived first, so a
    learner always has exactly one active path to track progress against.
    """
    result = _engine.generate_recommendations(profile_data, db, top_n=top_n)
    roadmap = result["learning_path"]

    profile = _get_or_create_profile(user_id, profile_data, db)

    # Archive any existing active path before starting a new one.
    db.query(LearningPath).filter(
        LearningPath.profile_id == profile.id,
        LearningPath.status == "active",
    ).update({"status": "archived"})

    career = db.query(Career).filter(Career.slug == result["career_slug"]).first()

    path = LearningPath(
        profile_id=profile.id,
        career_id=career.id if career else None,
        title=f"{result['target_career']} Learning Path",
        status="active",
        total_estimated_hours=roadmap.get("total_estimated_hours", 0.0),
    )
    db.add(path)
    db.flush()  # populate path.id for PathItem FKs

    for item in roadmap.get("sequence", []):
        db.add(PathItem(
            path_id=path.id,
            course_id=item.get("course_id"),
            item_type=item.get("item_type", "course"),
            title=item.get("title", ""),
            phase_number=item.get("phase_number", 1),
            sequence_order=item.get("sequence_order", 1),
            status="not_started",
            is_prerequisite_satisfied=not item.get("missing_prerequisites"),
        ))

    db.commit()
    db.refresh(path)
    return path
