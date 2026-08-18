from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    target_role = Column(String(100), nullable=True, index=True)
    weekly_hours = Column(Integer, default=10, nullable=False)
    experience_level = Column(String(50), default="beginner", nullable=False) # beginner, intermediate, advanced
    preferred_learning_style = Column(String(50), default="mixed", nullable=False) # video, text, project, mixed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="profile")
    skills = relationship("UserSkill", back_populates="profile", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="profile", cascade="all, delete-orphan")


class UserSkill(Base):
    __tablename__ = "user_skills"
    __table_args__ = (
        CheckConstraint("proficiency_level >= 1 AND proficiency_level <= 5", name="check_user_skill_proficiency_range"),
        UniqueConstraint("profile_id", "skill_id", name="uq_user_profile_skill"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("learner_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    proficiency_level = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    profile = relationship("LearnerProfile", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")
