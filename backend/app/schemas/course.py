from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.schemas.skill import SkillRead

class CourseSkillBase(BaseModel):
    skill_id: int
    level_gained: int = Field(default=1, ge=1, le=5)
    is_primary: bool = True

class CourseSkillCreate(CourseSkillBase):
    course_id: int

class CourseSkillRead(CourseSkillBase):
    id: int
    course_id: int
    skill: Optional[SkillRead] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None
    provider: str
    url: Optional[str] = None
    resource_type: str = "course" # course, project, assessment, practice, tutorial
    learning_format: str = "interactive" # video, text, interactive, project
    is_project_based: bool = False
    duration_hours: float = Field(..., gt=0)
    difficulty_level: str = "intermediate"
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[str] = None
    url: Optional[str] = None
    resource_type: Optional[str] = None
    learning_format: Optional[str] = None
    is_project_based: Optional[bool] = None
    duration_hours: Optional[float] = Field(default=None, gt=0)
    difficulty_level: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)

class CourseRead(CourseBase):
    id: int
    course_skills: List[CourseSkillRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
