"""
Response schemas for the progress dashboard and adaptation signals endpoints.
Additive — does not modify schemas/progress.py or schemas/feedback.py.
"""
from typing import List, Optional
from pydantic import BaseModel


class ProgressDashboardResponse(BaseModel):
    total_resources: int
    completed_resources: int
    in_progress_resources: int
    overall_completion_pct: float
    total_learning_hours: float
    completed_learning_hours: float
    current_learning_phase: Optional[int] = None
    current_resource: Optional[str] = None


class AdaptationSignalsResponse(BaseModel):
    user_id: int
    completed_resources: List[str]
    needs_foundation_support: List[str]
    accelerate_skills: List[str]
    deprioritize_skills: List[str]
