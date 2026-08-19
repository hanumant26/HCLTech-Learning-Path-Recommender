"""
POST /api/learning-path — Return only the learning path roadmap portion.

Phase 4 design decision: POST (not GET) because the learning path is dynamically
generated from a learner profile and is stateless — there is no server-side session
to look up. Accepts the same LearnerProfileRequest body as the recommendations
endpoint and returns only the `learning_path` block.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.services.recommendation_engine import RecommendationEngine
from backend.app.schemas.api_responses import LearnerProfileRequest, LearningPathResponse

router = APIRouter()

_engine = RecommendationEngine()


@router.post(
    "/learning-path",
    response_model=LearningPathResponse,
    status_code=200,
    summary="Generate a personalized learning path roadmap",
    description=(
        "Runs the full recommendation pipeline and returns only the structured "
        "multi-phase learning path roadmap (phases, sequence, time estimates). "
        "For the complete result including ranked recommendations and skill gap report, "
        "use POST /api/recommendations/generate instead."
    ),
)
def generate_learning_path(
    body: LearnerProfileRequest,
    top_n: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Number of top recommendations to include in the path (1–50, default 10)",
    ),
    db: Session = Depends(get_db),
) -> LearningPathResponse:
    """
    Delegates to RecommendationEngine.generate_recommendations() and extracts
    the learning_path key. Reuses the same pipeline so the roadmap is always
    consistent with the ranked recommendations.
    """
    profile_data = body.model_dump()
    result = _engine.generate_recommendations(profile_data, db, top_n=top_n)
    return result["learning_path"]
