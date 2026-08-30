from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class UserSkillBase(BaseModel):
    skill_id: int
    proficiency_level: int = Field(..., ge=1, le=5, description="Proficiency level from 1 (Novice) to 5 (Expert)")

class UserSkillCreate(UserSkillBase):
    profile_id: int

class UserSkillUpdate(BaseModel):
    proficiency_level: int = Field(..., ge=1, le=5)

class UserSkillRead(UserSkillBase):
    id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LearnerProfileBase(BaseModel):
    target_role: Optional[str] = None
    weekly_hours: int = Field(default=10, ge=1, le=168)
    experience_level: str = "beginner"
    preferred_learning_style: str = "mixed"

class LearnerProfileCreate(LearnerProfileBase):
    user_id: int

class LearnerProfileUpdate(BaseModel):
    target_role: Optional[str] = None
    weekly_hours: Optional[int] = Field(default=None, ge=1, le=168)
    experience_level: Optional[str] = None
    preferred_learning_style: Optional[str] = None

class LearnerProfileRead(LearnerProfileBase):
    id: int
    user_id: int
    skills: List[UserSkillRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
