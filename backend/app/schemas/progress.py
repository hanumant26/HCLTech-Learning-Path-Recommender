from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ProgressBase(BaseModel):
    completion_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    time_spent_mins: int = Field(default=0, ge=0)

class ProgressCreate(ProgressBase):
    path_item_id: int

class ProgressUpdate(BaseModel):
    completion_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    time_spent_mins: Optional[int] = Field(default=None, ge=0)
    completed_at: Optional[datetime] = None

class ProgressRead(ProgressBase):
    id: int
    path_item_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
