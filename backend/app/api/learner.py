"""
POST /api/learner/profile — Validate and normalize a learner profile.

Phase 4 design decision: validation-only, nothing is persisted to the database.
The LearnerProfile DB model requires a user_id FK (auth not yet implemented in Phase 4).
Persistence will be added in Phase 5 once authentication is in place.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.career import Career
from backend.app.services.exceptions import UnknownCareerError
from backend.app.services.recommendation_engine import RecommendationEngine
from backend.app.schemas.api_responses import LearnerProfileRequest, LearnerProfileResponse

router = APIRouter()

_engine = RecommendationEngine()


@router.post(
    "/learner/profile",
    response_model=LearnerProfileResponse,
    status_code=200,
    summary="Validate a learner profile",
    description=(
        "Validates and normalizes a learner profile payload. "
        "No data is persisted — this endpoint is a client-side validation helper. "
        "Use the returned `normalized_profile` as input to `/api/recommendations/generate`."
    ),
)
def validate_learner_profile(
    body: LearnerProfileRequest,
    db: Session = Depends(get_db),
) -> LearnerProfileResponse:
    """
    Validate profile via the existing RecommendationEngine normalizer.
    Service exceptions (InvalidProfileError, UnknownCareerError) are caught
    by the global exception handlers registered in main.py.
    """
    profile_data = body.model_dump()

    # validate_and_normalize_profile raises InvalidProfileError or UnknownCareerError
    # on bad input — these propagate to the global exception handlers.
    normalized = _engine.validate_and_normalize_profile(profile_data)

    target_career = normalized["target_career"]
    career = db.query(Career).filter(
        (Career.slug == target_career.lower().strip()) |
        (Career.title.ilike(target_career.strip()))
    ).first()
    if not career:
        raise UnknownCareerError(f"Target career '{target_career}' not found in database.")

    return LearnerProfileResponse(
        valid=True,
        normalized_profile=normalized,
        message="Learner profile is valid and normalized.",
    )

