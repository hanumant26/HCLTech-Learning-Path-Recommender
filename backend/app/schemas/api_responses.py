"""
Phase 4 API request/response schemas.

These are purpose-built for the HTTP API layer and do NOT replace the existing
CRUD schemas used by internal services. Business logic remains in the service layer.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request Body
# ---------------------------------------------------------------------------

class LearnerProfileRequest(BaseModel):
    """
    Unified request body for:
      - POST /api/learner/profile  (validation only)
      - POST /api/recommendations/generate
      - POST /api/learning-path
    """
    target_career: str = Field(
        ...,
        description="Career slug (e.g. 'data-scientist') or title (e.g. 'Data Scientist')",
        examples=["Data Scientist"],
    )
    weekly_hours: int = Field(
        default=10,
        ge=1,
        le=168,
        description="Hours available per week for learning (1–168)",
    )
    skills: Dict[str, int] = Field(
        default_factory=dict,
        description="Current skill proficiencies — {skill_name_or_slug: level 0-5}",
        examples=[{"Python": 3, "SQL": 2}],
    )
    completed_resources: List[str] = Field(
        default_factory=list,
        description="Slugs or titles of already-completed courses/resources to exclude",
    )
    preferred_learning_style: str = Field(
        default="mixed",
        description="Preferred format: 'video', 'text', 'project', or 'mixed'",
    )
    interests: List[str] = Field(
        default_factory=list,
        description="Optional free-form interest tags",
    )


# ---------------------------------------------------------------------------
# GET /api/careers
# ---------------------------------------------------------------------------

class CareerSummary(BaseModel):
    """Lightweight career representation for listing."""
    id: int
    slug: str
    title: str
    description: Optional[str] = None
    required_skills_count: int


class CareersResponse(BaseModel):
    careers: List[CareerSummary]
    total: int


# ---------------------------------------------------------------------------
# GET /api/skills
# ---------------------------------------------------------------------------

class SkillSummary(BaseModel):
    """Lightweight skill representation for listing."""
    id: int
    slug: str
    name: str
    category: str
    description: Optional[str] = None


class SkillsResponse(BaseModel):
    skills: List[SkillSummary]
    total: int


# ---------------------------------------------------------------------------
# POST /api/learner/profile  (transient validation — nothing persisted)
# ---------------------------------------------------------------------------

class LearnerProfileResponse(BaseModel):
    valid: bool
    normalized_profile: Dict[str, Any]
    message: str


# ---------------------------------------------------------------------------
# POST /api/recommendations/generate  &  POST /api/learning-path
# ---------------------------------------------------------------------------

class SkillGapSummary(BaseModel):
    career_id: int
    career_slug: str
    career_title: str
    total_required_skills: int
    proficient_count: int
    minor_gap_count: int
    critical_gap_count: int
    total_gap_points: int
    readiness_percentage: float


class SkillGapItem(BaseModel):
    skill_id: int
    skill: str
    skill_slug: str
    category: str
    current_level: int
    required_level: int
    gap: int
    status: str          # proficient | minor | critical
    importance: str      # critical | high | medium | optional
    is_core: bool


class SkillGapReport(BaseModel):
    summary: SkillGapSummary
    skill_gaps: List[SkillGapItem]


class ScoreBreakdown(BaseModel):
    goal_relevance: float
    skill_gap: float
    prerequisite_readiness: float
    semantic_similarity: float
    difficulty_match: float
    time_fit: float
    quality: float


class RecommendationItem(BaseModel):
    resource_id: int
    slug: str
    title: str
    provider: str
    resource_type: str
    difficulty_level: str
    duration_hours: float
    rating: Optional[float] = None
    score: float
    breakdown: ScoreBreakdown
    reason_codes: List[str]
    target_skills: List[Any]
    prerequisites: List[str]
    missing_prerequisites: List[Any]
    readiness_status: str


class RoadmapItem(BaseModel):
    course_id: Optional[int] = None
    slug: str
    title: str
    provider: str
    item_type: str
    difficulty_level: str
    estimated_hours: float
    score: Optional[float] = None
    readiness_status: str
    missing_prerequisites: List[Any]
    target_skills: List[str]
    reason_codes: List[str]
    sequence_order: Optional[int] = None
    phase_number: Optional[int] = None
    phase_name: Optional[str] = None



class RoadmapPhase(BaseModel):
    phase_number: int
    phase_name: str
    items: List[RoadmapItem]
    phase_hours: float


class LearningPathResponse(BaseModel):
    phases: List[RoadmapPhase]
    sequence: List[RoadmapItem]
    total_items: int
    total_estimated_hours: float
    total_estimated_weeks: float
    weekly_hours: int
    locked_items: List[RoadmapItem]


class RecommendationsResponse(BaseModel):
    target_career: str
    career_slug: str
    weekly_hours: int
    skill_gap_report: SkillGapReport
    total_candidates_found: int
    recommendations: List[RecommendationItem]
    learning_path: LearningPathResponse


# ---------------------------------------------------------------------------
# Shared error response shape (used by exception handlers in main.py)
# ---------------------------------------------------------------------------

class ErrorResponse(BaseModel):
    detail: str
    error_type: str
