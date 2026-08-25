"""
Feedback Service (Progress/Feedback/Adaptation module).

Owns creation/retrieval of Feedback records against existing PathItem rows.
Reuses the existing Feedback model — no new tables.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from backend.app.models.feedback import Feedback
from backend.app.models.learning_path import PathItem
from backend.app.models.user import User
from backend.app.schemas.feedback import FeedbackCreate
from backend.app.services.exceptions import (
    PathItemNotFoundError,
    InvalidFeedbackTypeError,
    InvalidProfileError,
)

VALID_RATING_TYPES = {"too_easy", "appropriate", "too_difficult", "not_relevant"}


def submit_feedback(data: FeedbackCreate, db: Session) -> Feedback:
    """POST /api/feedback — validates resource, user, and feedback type."""
    if not db.query(PathItem.id).filter(PathItem.id == data.path_item_id).first():
        raise PathItemNotFoundError(f"Path item {data.path_item_id} not found.")

    if not db.query(User.id).filter(User.id == data.user_id).first():
        raise InvalidProfileError(f"User {data.user_id} does not exist.")

    rating_type = data.rating_type.strip().lower()
    if rating_type not in VALID_RATING_TYPES:
        raise InvalidFeedbackTypeError(
            f"'{data.rating_type}' is not a supported feedback type. "
            f"Expected one of: {sorted(VALID_RATING_TYPES)}."
        )

    feedback = Feedback(
        path_item_id=data.path_item_id,
        user_id=data.user_id,
        rating_type=rating_type,
        comment=data.comment,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def get_feedback_history(user_id: int, db: Session) -> List[Feedback]:
    """GET /api/feedback — learner's full feedback history, most recent first."""
    return (
        db.query(Feedback)
        .filter(Feedback.user_id == user_id)
        .order_by(Feedback.created_at.desc())
        .all()
    )


def get_feedback_for_item(path_item_id: int, db: Session) -> List[Feedback]:
    """GET /api/feedback/{resource_id} — feedback submitted for one resource."""
    if not db.query(PathItem.id).filter(PathItem.id == path_item_id).first():
        raise PathItemNotFoundError(f"Path item {path_item_id} not found.")
    return (
        db.query(Feedback)
        .filter(Feedback.path_item_id == path_item_id)
        .order_by(Feedback.created_at.desc())
        .all()
    )
