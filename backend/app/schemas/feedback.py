from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class FeedbackBase(BaseModel):
    rating_type: str # too_easy, appropriate, too_difficult, not_relevant
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    path_item_id: int
    user_id: int

class FeedbackRead(FeedbackBase):
    id: int
    path_item_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
