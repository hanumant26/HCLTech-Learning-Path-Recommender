from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class AssessmentResultBase(BaseModel):
    score_pct: float = Field(..., ge=0.0, le=100.0)
    passed: bool
    attempt_number: int = Field(default=1, ge=1)

class AssessmentResultCreate(AssessmentResultBase):
    assessment_id: int
    user_id: int

class AssessmentResultRead(AssessmentResultBase):
    id: int
    assessment_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    passing_score_pct: float = Field(default=70.0, ge=0.0, le=100.0)
    path_item_id: Optional[int] = None
    skill_id: Optional[int] = None
    questions: Optional[List[Dict[str, Any]]] = None

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentRead(AssessmentBase):
    id: int
    results: List[AssessmentResultRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
