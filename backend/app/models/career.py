from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(100), unique=True, nullable=False) # Data Scientist, AI Engineer, Machine Learning Engineer, Data Analyst, Full Stack Developer
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    career_skills = relationship("CareerSkill", back_populates="career", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="career")


class CareerSkill(Base):
    __tablename__ = "career_skills"
    __table_args__ = (
        CheckConstraint("required_level >= 1 AND required_level <= 5", name="check_career_skill_level_range"),
        UniqueConstraint("career_id", "skill_id", name="uq_career_skill"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    required_level = Column(Integer, nullable=False)
    importance = Column(String(20), default="high", nullable=False) # critical, high, medium, optional
    is_core = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    career = relationship("Career", back_populates="career_skills")
    skill = relationship("Skill", back_populates="career_skills")
