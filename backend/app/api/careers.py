"""
GET /api/careers — List all careers with skill requirement counts.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.career import Career
from backend.app.schemas.api_responses import CareerSummary, CareersResponse

router = APIRouter()


@router.get(
    "/careers",
    response_model=CareersResponse,
    summary="List all available careers",
    description=(
        "Returns every career in the knowledge base along with a count of its required skills. "
        "Use the `slug` or `title` values as `target_career` in the recommendation endpoints."
    ),
)
def list_careers(
    db: Session = Depends(get_db),
) -> CareersResponse:
    """Retrieve all careers from the database."""
    careers = db.query(Career).order_by(Career.title).all()

    career_summaries = [
        CareerSummary(
            id=career.id,
            slug=career.slug,
            title=career.title,
            description=career.description,
            required_skills_count=len(career.career_skills),
        )
        for career in careers
    ]

    return CareersResponse(careers=career_summaries, total=len(career_summaries))
