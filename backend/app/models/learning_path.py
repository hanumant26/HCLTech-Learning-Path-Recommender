from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("learner_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(200), nullable=False)
    status = Column(String(50), default="active", nullable=False) # active, completed, archived
    total_estimated_hours = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    profile = relationship("LearnerProfile", back_populates="learning_paths")
    career = relationship("Career", back_populates="learning_paths")
    path_items = relationship("PathItem", back_populates="path", cascade="all, delete-orphan", order_by="PathItem.sequence_order")


class PathItem(Base):
    __tablename__ = "path_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="SET NULL"), nullable=True, index=True)
    item_type = Column(String(50), default="course", nullable=False) # course, project, assessment, prerequisite_filler
    title = Column(String(200), nullable=False)
    phase_number = Column(Integer, default=1, nullable=False)
    sequence_order = Column(Integer, default=1, nullable=False)
    status = Column(String(50), default="not_started", nullable=False) # not_started, in_progress, completed, skipped
    is_prerequisite_satisfied = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    path = relationship("LearningPath", back_populates="path_items")
    course = relationship("Course", back_populates="path_items")
    progress = relationship("Progress", back_populates="path_item", uselist=False, cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="path_item", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="path_item", cascade="all, delete-orphan")
