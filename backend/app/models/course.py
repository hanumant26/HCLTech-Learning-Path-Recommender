from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Course(Base):
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint("rating IS NULL OR (rating >= 0.0 AND rating <= 5.0)", name="check_course_rating_range"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    provider = Column(String(100), nullable=False, index=True)
    url = Column(String(500), nullable=True)
    resource_type = Column(String(50), default="course", nullable=False) # course, project, assessment, practice, tutorial
    learning_format = Column(String(50), default="interactive", nullable=False) # video, text, interactive, project
    is_project_based = Column(Boolean, default=False, nullable=False)
    duration_hours = Column(Float, nullable=False)
    difficulty_level = Column(String(20), default="intermediate", nullable=False) # beginner, intermediate, advanced
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    course_skills = relationship("CourseSkill", back_populates="course", cascade="all, delete-orphan")
    path_items = relationship("PathItem", back_populates="course")


class CourseSkill(Base):
    __tablename__ = "course_skills"
    __table_args__ = (
        CheckConstraint("level_gained >= 1 AND level_gained <= 5", name="check_course_skill_level_gained"),
        UniqueConstraint("course_id", "skill_id", name="uq_course_skill"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    level_gained = Column(Integer, default=1, nullable=False)
    is_primary = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="course_skills")
    skill = relationship("Skill", back_populates="course_skills")
