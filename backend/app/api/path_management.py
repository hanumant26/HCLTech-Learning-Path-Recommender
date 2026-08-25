"""
Path Management API — additive, kept separate from the existing
api/learning_path.py (which stays untouched, per the guide).

POST /api/learning-path/start        — Persist a generated roadmap so a
                                         learner can start tracking progress.
GET  /api/learning-path/adaptation    — Learner-state signals derived from
                                         stored Progress + Feedback, ready to
                                         feed back into the existing engine.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.path_management import StartLearningPathRequest, StartLearningPathResponse
from backend.app.schemas.dashboard import AdaptationSignalsResponse
from backend.app.services import path_persistence_service, adaptation_service

router = APIRouter()


@router.post(
    "/learning-path/start",
    response_model=StartLearningPathResponse,
    status_code=201,
    summary="Persist a generated learning path so progress can be tracked",
    description=(
        "Runs the existing recommendation pipeline (unchanged) and saves the "
        "resulting roadmap as a LearningPath with PathItem rows, so subsequent "
        "POST /api/progress and POST /api/feedback calls have real resource IDs "
        "to reference. Archives any previously active path for this learner."
    ),
)
def start_learning_path(
    body: StartLearningPathRequest,
    db: Session = Depends(get_db),
) -> StartLearningPathResponse:
    profile_data = body.profile.model_dump()
    path = path_persistence_service.start_learning_path(body.user_id, profile_data, db)
    return StartLearningPathResponse(
        path_id=path.id,
        title=path.title,
        status=path.status,
        total_estimated_hours=path.total_estimated_hours,
        created_at=path.created_at,
        items=[
            {
                "id": item.id,
                "title": item.title,
                "item_type": item.item_type,
                "phase_number": item.phase_number,
                "sequence_order": item.sequence_order,
                "status": item.status,
            }
            for item in sorted(path.path_items, key=lambda i: i.sequence_order)
        ],
    )


@router.get(
    "/learning-path/adaptation",
    response_model=AdaptationSignalsResponse,
    status_code=200,
    summary="Get learner-state adaptation signals",
    description=(
        "Interprets stored Progress + Feedback into signals for the existing "
        "recommendation engine. `completed_resources` can be passed directly "
        "into the engine's existing completed_resources input; the skill lists "
        "are advisory for how future recommendations should adapt."
    ),
)
def get_adaptation_signals(
    user_id: int = Query(..., description="Learner's user_id"),
    db: Session = Depends(get_db),
) -> AdaptationSignalsResponse:
    return adaptation_service.get_adaptation_signals(user_id, db)
