"""
GET /api/skills — List all skills, optionally filtered by category.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.skill import Skill
from backend.app.schemas.api_responses import SkillSummary, SkillsResponse

router = APIRouter()


@router.get(
    "/skills",
    response_model=SkillsResponse,
    summary="List all skills",
    description=(
        "Returns every skill in the knowledge base. "
        "Use the `slug` or `name` values as keys in the `skills` dict when submitting a learner profile."
    ),
)
def list_skills(
    category: Optional[str] = Query(
        default=None,
        description="Filter by category, e.g. 'Programming Language', 'Framework', 'Concept', 'Tool'",
    ),
    db: Session = Depends(get_db),
) -> SkillsResponse:
    """Retrieve all skills, with optional category filtering."""
    query = db.query(Skill).order_by(Skill.category, Skill.name)

    if category:
        query = query.filter(Skill.category.ilike(f"%{category}%"))

    skills = query.all()

    skill_summaries = [
        SkillSummary(
            id=skill.id,
            slug=skill.slug,
            name=skill.name,
            category=skill.category,
            description=skill.description,
        )
        for skill in skills
    ]

    return SkillsResponse(skills=skill_summaries, total=len(skill_summaries))
