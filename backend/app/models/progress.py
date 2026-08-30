from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (
        CheckConstraint("completion_pct >= 0.0 AND completion_pct <= 100.0", name="check_completion_pct_range"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path_item_id = Column(Integer, ForeignKey("path_items.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    completion_pct = Column(Float, default=0.0, nullable=False)
    time_spent_mins = Column(Integer, default=0, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    path_item = relationship("PathItem", back_populates="progress")
