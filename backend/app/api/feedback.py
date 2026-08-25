"""
Feedback API (guide section 7).

POST  /api/feedback               — Submit feedback.
GET   /api/feedback                — Retrieve learner feedback history.
GET   /api/feedback/{resource_id}  — Retrieve feedback for a resource.
"""
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.feedback import FeedbackCreate, FeedbackRead
from backend.app.services import feedback_service

router = APIRouter()


@router.post(
    "/feedback",
    response_model=FeedbackRead,
    status_code=201,
    summary="Submit feedback for a resource",
)
def submit_feedback(body: FeedbackCreate, db: Session = Depends(get_db)) -> FeedbackRead:
    return feedback_service.submit_feedback(body, db)


@router.get(
    "/feedback",
    response_model=List[FeedbackRead],
    status_code=200,
    summary="Retrieve learner feedback history",
)
def get_feedback_history(
    user_id: int = Query(..., description="Learner's user_id"),
    db: Session = Depends(get_db),
) -> List[FeedbackRead]:
    return feedback_service.get_feedback_history(user_id, db)


@router.get(
    "/feedback/{resource_id}",
    response_model=List[FeedbackRead],
    status_code=200,
    summary="Retrieve feedback for a resource",
)
def get_feedback_for_resource(resource_id: int, db: Session = Depends(get_db)) -> List[FeedbackRead]:
    return feedback_service.get_feedback_for_item(resource_id, db)
