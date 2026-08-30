from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.schemas.course import CourseRead

class PathItemBase(BaseModel):
    course_id: Optional[int] = None
    item_type: str = "course" # course, project, assessment, prerequisite_filler
    title: str
    phase_number: int = Field(default=1, ge=1)
    sequence_order: int = Field(default=1, ge=1)
    status: str = "not_started"
    is_prerequisite_satisfied: bool = True

class PathItemCreate(PathItemBase):
    path_id: int

class PathItemUpdate(BaseModel):
    status: Optional[str] = None
    phase_number: Optional[int] = Field(default=None, ge=1)
    sequence_order: Optional[int] = Field(default=None, ge=1)
    is_prerequisite_satisfied: Optional[bool] = None

class PathItemRead(PathItemBase):
    id: int
    path_id: int
    course: Optional[CourseRead] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LearningPathBase(BaseModel):
    title: str
    career_id: Optional[int] = None
    status: str = "active"
    total_estimated_hours: float = 0.0

class LearningPathCreate(LearningPathBase):
    profile_id: int

class LearningPathRead(LearningPathBase):
    id: int
    profile_id: int
    path_items: List[PathItemRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
