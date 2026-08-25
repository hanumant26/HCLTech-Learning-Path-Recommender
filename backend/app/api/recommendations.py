"""
POST /api/recommendations/generate — Execute the full recommendation pipeline.

Orchestrates skill gap analysis, prerequisite resolution, candidate retrieval,
multi-factor scoring, ranking, and learning path roadmap generation — all delegated
to the existing RecommendationEngine service. This router contains zero business logic.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.services.recommendation_engine import RecommendationEngine
from backend.app.schemas.api_responses import LearnerProfileRequest, RecommendationsResponse

router = APIRouter()

_engine = RecommendationEngine()


@router.post(
    "/recommendations/generate",
    response_model=RecommendationsResponse,
    status_code=200,
    summary="Generate personalized learning recommendations",
    description=(
        "Runs the complete 8-step recommendation pipeline: "
        "skill gap analysis → prerequisite resolution → candidate retrieval → "
        "multi-factor scoring → deterministic ranking → learning path roadmap generation. "
        "Returns ranked course recommendations and an ordered multi-phase learning roadmap."
    ),
)
def generate_recommendations(
    body: LearnerProfileRequest,
    top_n: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of top recommendations to return (1–50, default 10)",
    ),
    db: Session = Depends(get_db),
) -> RecommendationsResponse:
    """
    Delegate entirely to RecommendationEngine.generate_recommendations().
    Service exceptions are handled by global exception handlers in main.py:
      - InvalidProfileError  → HTTP 422
      - UnknownCareerError   → HTTP 404
      - NoCandidateResourcesError → HTTP 404
      - RecommendationEngineError (base) → HTTP 500
    """
    profile_data = body.model_dump()
    result = _engine.generate_recommendations(profile_data, db, top_n=top_n)
    return result
