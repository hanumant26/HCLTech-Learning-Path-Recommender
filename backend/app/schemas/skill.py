from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class SkillBase(BaseModel):
    slug: str
    name: str
    category: str
    description: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    slug: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class SkillRead(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SkillPrerequisiteBase(BaseModel):
    skill_id: int
    prerequisite_skill_id: int
    required_level: int = Field(default=1, ge=1, le=5)

class SkillPrerequisiteCreate(SkillPrerequisiteBase):
    pass

class SkillPrerequisiteRead(SkillPrerequisiteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
