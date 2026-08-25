from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False, index=True) # Programming Language, Framework, Concept, Tool
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")
    career_skills = relationship("CareerSkill", back_populates="skill", cascade="all, delete-orphan")
    course_skills = relationship("CourseSkill", back_populates="skill", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="skill", cascade="all, delete-orphan")

    # Self-referential prerequisite relationships
    prerequisites = relationship(
        "SkillPrerequisite",
        foreign_keys="SkillPrerequisite.skill_id",
        back_populates="skill",
        cascade="all, delete-orphan"
    )
    dependent_skills = relationship(
        "SkillPrerequisite",
        foreign_keys="SkillPrerequisite.prerequisite_skill_id",
        back_populates="prerequisite_skill",
        cascade="all, delete-orphan"
    )


class SkillPrerequisite(Base):
    __tablename__ = "skill_prerequisites"
    __table_args__ = (
        CheckConstraint("required_level >= 1 AND required_level <= 5", name="check_prereq_level_range"),
        CheckConstraint("skill_id != prerequisite_skill_id", name="check_no_self_prerequisite"),
        UniqueConstraint("skill_id", "prerequisite_skill_id", name="uq_skill_prerequisite"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    prerequisite_skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    required_level = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    skill = relationship("Skill", foreign_keys=[skill_id], back_populates="prerequisites")
    prerequisite_skill = relationship("Skill", foreign_keys=[prerequisite_skill_id], back_populates="dependent_skills")
