from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.schemas.skill import SkillRead

class CareerSkillBase(BaseModel):
    skill_id: int
    required_level: int = Field(..., ge=1, le=5, description="Required skill level from 1 to 5")
    importance: str = Field(default="high", pattern="^(critical|high|medium|optional)$")
    is_core: bool = True

class CareerSkillCreate(CareerSkillBase):
    career_id: int

class CareerSkillRead(CareerSkillBase):
    id: int
    career_id: int
    skill: Optional[SkillRead] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CareerBase(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None

class CareerCreate(CareerBase):
    pass

class CareerRead(CareerBase):
    id: int
    career_skills: List[CareerSkillRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
