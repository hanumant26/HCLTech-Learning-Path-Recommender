"""
Schemas for POST /api/learning-path/start.

Additive — reuses LearnerProfileRequest from schemas/api_responses.py rather
than duplicating its fields.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from backend.app.schemas.api_responses import LearnerProfileRequest


class StartLearningPathRequest(BaseModel):
    """Body for POST /api/learning-path/start."""
    user_id: int
    profile: LearnerProfileRequest


class PathItemSummary(BaseModel):
    id: int
    title: str
    item_type: str
    phase_number: int
    sequence_order: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class StartLearningPathResponse(BaseModel):
    path_id: int
    title: str
    status: str
    total_estimated_hours: float
    created_at: datetime
    items: List[PathItemSummary]

    model_config = ConfigDict(from_attributes=True)
