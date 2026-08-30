"""
Progress Service (Progress/Feedback/Adaptation module).

Owns creation/update of Progress records against existing PathItem rows,
and computes the aggregate dashboard view for a learner. Reuses the
existing Progress, PathItem, LearningPath, and LearnerProfile models —
no new tables.
"""
from datetime import datetime, timezone
from typing import Dict, Optional
from sqlalchemy.orm import Session

from backend.app.models.progress import Progress
from backend.app.models.learning_path import PathItem, LearningPath
from backend.app.models.profile import LearnerProfile
from backend.app.schemas.progress import ProgressCreate, ProgressUpdate
from backend.app.services.exceptions import PathItemNotFoundError, LearnerProfileNotFoundError


def _get_path_item_or_raise(path_item_id: int, db: Session) -> PathItem:
    item = db.query(PathItem).filter(PathItem.id == path_item_id).first()
    if not item:
        raise PathItemNotFoundError(f"Path item {path_item_id} not found.")
    return item


def _sync_item_status(item: PathItem, completion_pct: float) -> None:
    """Keeps PathItem.status consistent with the Progress record driving it."""
    if completion_pct <= 0.0:
        item.status = "not_started"
    elif completion_pct >= 100.0:
        item.status = "completed"
    else:
        item.status = "in_progress"


def create_or_update_progress(data: ProgressCreate, db: Session) -> Progress:
    """
    Progress.path_item_id is unique — one record per item — so POST is
    idempotent create-or-update, matching the guide's `POST /api/progress`.
    """
    item = _get_path_item_or_raise(data.path_item_id, db)

    progress = db.query(Progress).filter(Progress.path_item_id == data.path_item_id).first()
    if progress is None:
        progress = Progress(path_item_id=data.path_item_id)
        db.add(progress)

    progress.completion_pct = data.completion_pct
    progress.time_spent_mins = data.time_spent_mins
    if data.completion_pct >= 100.0 and progress.completed_at is None:
        progress.completed_at = datetime.now(timezone.utc)
    elif data.completion_pct < 100.0:
        progress.completed_at = None

    _sync_item_status(item, data.completion_pct)

    db.commit()
    db.refresh(progress)
    return progress


def update_progress(path_item_id: int, data: ProgressUpdate, db: Session) -> Progress:
    """Partial update — PUT /api/progress/{path_item_id}."""
    item = _get_path_item_or_raise(path_item_id, db)
    progress = db.query(Progress).filter(Progress.path_item_id == path_item_id).first()
    if progress is None:
        raise PathItemNotFoundError(
            f"No progress record exists yet for path item {path_item_id}. POST /api/progress first."
        )

    if data.completion_pct is not None:
        progress.completion_pct = data.completion_pct
        _sync_item_status(item, data.completion_pct)
        if data.completion_pct >= 100.0 and progress.completed_at is None:
            progress.completed_at = datetime.now(timezone.utc)
        elif data.completion_pct < 100.0:
            progress.completed_at = None
    if data.time_spent_mins is not None:
        progress.time_spent_mins = data.time_spent_mins
    if data.completed_at is not None:
        progress.completed_at = data.completed_at

    db.commit()
    db.refresh(progress)
    return progress


def get_progress_for_item(path_item_id: int, db: Session) -> Optional[Progress]:
    _get_path_item_or_raise(path_item_id, db)
    return db.query(Progress).filter(Progress.path_item_id == path_item_id).first()


def get_overall_progress(user_id: int, db: Session) -> Dict:
    """
    Dashboard aggregate (guide section 13): total/completed/in-progress
    resources, overall completion %, learning hours, current phase/resource
    — computed from the learner's most recent active LearningPath.
    """
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user_id).first()
    if not profile:
        raise LearnerProfileNotFoundError(f"No learner profile found for user {user_id}.")

    path = (
        db.query(LearningPath)
        .filter(LearningPath.profile_id == profile.id, LearningPath.status == "active")
        .order_by(LearningPath.created_at.desc())
        .first()
    )
    if not path:
        return {
            "total_resources": 0,
            "completed_resources": 0,
            "in_progress_resources": 0,
            "overall_completion_pct": 0.0,
            "total_learning_hours": 0.0,
            "completed_learning_hours": 0.0,
            "current_learning_phase": None,
            "current_resource": None,
        }

    items = sorted(path.path_items, key=lambda i: i.sequence_order)
    total = len(items)
    completed = sum(1 for i in items if i.status == "completed")
    in_progress = sum(1 for i in items if i.status == "in_progress")

    completed_hours = 0.0
    current_item = None
    for i in items:
        if i.status == "completed" and i.course:
            completed_hours += i.course.duration_hours or 0.0
        if i.status != "completed" and current_item is None:
            current_item = i

    overall_pct = round((completed / total) * 100, 1) if total else 0.0

    return {
        "total_resources": total,
        "completed_resources": completed,
        "in_progress_resources": in_progress,
        "overall_completion_pct": overall_pct,
        "total_learning_hours": round(path.total_estimated_hours or 0.0, 1),
        "completed_learning_hours": round(completed_hours, 1),
        "current_learning_phase": current_item.phase_number if current_item else None,
        "current_resource": current_item.title if current_item else None,
    }
