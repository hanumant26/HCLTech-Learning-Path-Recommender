from backend.app.schemas.user import UserBase, UserCreate, UserUpdate, UserRead
from backend.app.schemas.profile import (
    LearnerProfileBase, LearnerProfileCreate, LearnerProfileUpdate, LearnerProfileRead,
    UserSkillBase, UserSkillCreate, UserSkillUpdate, UserSkillRead
)
from backend.app.schemas.skill import (
    SkillBase, SkillCreate, SkillUpdate, SkillRead,
    SkillPrerequisiteBase, SkillPrerequisiteCreate, SkillPrerequisiteRead
)
from backend.app.schemas.career import (
    CareerBase, CareerCreate, CareerRead,
    CareerSkillBase, CareerSkillCreate, CareerSkillRead
)
from backend.app.schemas.course import (
    CourseBase, CourseCreate, CourseUpdate, CourseRead,
    CourseSkillBase, CourseSkillCreate, CourseSkillRead
)
from backend.app.schemas.learning_path import (
    LearningPathBase, LearningPathCreate, LearningPathRead,
    PathItemBase, PathItemCreate, PathItemUpdate, PathItemRead
)
from backend.app.schemas.progress import ProgressBase, ProgressCreate, ProgressUpdate, ProgressRead
from backend.app.schemas.feedback import FeedbackBase, FeedbackCreate, FeedbackRead
from backend.app.schemas.assessment import (
    AssessmentBase, AssessmentCreate, AssessmentRead,
    AssessmentResultBase, AssessmentResultCreate, AssessmentResultRead
)

__all__ = [
    "UserBase", "UserCreate", "UserUpdate", "UserRead",
    "LearnerProfileBase", "LearnerProfileCreate", "LearnerProfileUpdate", "LearnerProfileRead",
    "UserSkillBase", "UserSkillCreate", "UserSkillUpdate", "UserSkillRead",
    "SkillBase", "SkillCreate", "SkillUpdate", "SkillRead",
    "SkillPrerequisiteBase", "SkillPrerequisiteCreate", "SkillPrerequisiteRead",
    "CareerBase", "CareerCreate", "CareerRead",
    "CareerSkillBase", "CareerSkillCreate", "CareerSkillRead",
    "CourseBase", "CourseCreate", "CourseUpdate", "CourseRead",
    "CourseSkillBase", "CourseSkillCreate", "CourseSkillRead",
    "LearningPathBase", "LearningPathCreate", "LearningPathRead",
    "PathItemBase", "PathItemCreate", "PathItemUpdate", "PathItemRead",
    "ProgressBase", "ProgressCreate", "ProgressUpdate", "ProgressRead",
    "FeedbackBase", "FeedbackCreate", "FeedbackRead",
    "AssessmentBase", "AssessmentCreate", "AssessmentRead",
    "AssessmentResultBase", "AssessmentResultCreate", "AssessmentResultRead",
]
