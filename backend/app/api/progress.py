"""
Progress API (guide section 5).

POST   /api/progress               — Create or update progress for a resource.
GET    /api/progress                — Retrieve learner overall progress (dashboard).
GET    /api/progress/{resource_id}  — Retrieve progress for one resource.
PUT    /api/progress/{resource_id}  — Update progress or status.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressRead
from backend.app.schemas.dashboard import ProgressDashboardResponse
from backend.app.services import progress_service

router = APIRouter()


@router.post(
    "/progress",
    response_model=ProgressRead,
    status_code=200,
    summary="Create or update progress for a resource",
)
def create_or_update_progress(body: ProgressCreate, db: Session = Depends(get_db)) -> ProgressRead:
    progress = progress_service.create_or_update_progress(body, db)
    return progress


@router.get(
    "/progress",
    response_model=ProgressDashboardResponse,
    status_code=200,
    summary="Retrieve learner overall progress (dashboard)",
)
def get_overall_progress(
    user_id: int = Query(..., description="Learner's user_id"),
    db: Session = Depends(get_db),
) -> ProgressDashboardResponse:
    return progress_service.get_overall_progress(user_id, db)


@router.get(
    "/progress/{resource_id}",
    response_model=ProgressRead,
    status_code=200,
    summary="Retrieve progress for one resource",
)
def get_progress_for_resource(resource_id: int, db: Session = Depends(get_db)) -> ProgressRead:
    progress = progress_service.get_progress_for_item(resource_id, db)
    if progress is None:
        # No progress record yet is a valid state (not_started) — return a zeroed shape
        # rather than a 404, since the resource itself exists.
        now = datetime.now(timezone.utc)
        return ProgressRead(
            id=0,
            path_item_id=resource_id,
            completion_pct=0.0,
            time_spent_mins=0,
            completed_at=None,
            created_at=now,
            updated_at=now,
        )
    return progress


@router.put(
    "/progress/{resource_id}",
    response_model=ProgressRead,
    status_code=200,
    summary="Update progress or status for a resource",
)
def update_progress(resource_id: int, body: ProgressUpdate, db: Session = Depends(get_db)) -> ProgressRead:
    return progress_service.update_progress(resource_id, body, db)
