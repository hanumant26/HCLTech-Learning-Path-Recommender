"""
Adaptation Service (Progress/Feedback/Adaptation module).

Interprets Progress + Feedback rows that are already stored and turns them
into learner-state signals. This service does NOT rank, score, or recommend
anything itself — it only prepares signals for the EXISTING RecommendationEngine
to consume (via its existing `completed_resources` input), matching the
guide's architecture rule:

    Progress + Feedback -> Learner State / Adaptation Signals
                         -> Existing Recommendation Engine
                         -> Updated Recommendations

No second recommendation engine, no rewritten scoring, no rewritten
prerequisite DAG.
"""
from typing import Any, Dict, List
from sqlalchemy.orm import Session

from backend.app.models.feedback import Feedback
from backend.app.models.progress import Progress
from backend.app.models.learning_path import PathItem, LearningPath
from backend.app.models.profile import LearnerProfile
from backend.app.models.course import Course
from backend.app.services.exceptions import LearnerProfileNotFoundError
from backend.app.services.prerequisite_engine import PrerequisiteEngine


def _interpret_feedback(rating_type: str) -> str:
    """Maps a raw feedback category to the adaptation action the guide defines."""
    return {
        "too_difficult": "needs_foundation_support",
        "too_easy": "ready_for_faster_progression",
        "appropriate": "continue_roadmap",
        "not_relevant": "deprioritize_similar",
    }.get(rating_type, "continue_roadmap")


def get_adaptation_signals(user_id: int, db: Session) -> Dict[str, Any]:
    """
    Builds the learner-state signal bundle for one learner:

    - completed_resources: slugs of fully-completed courses — feed this straight
      into RecommendationEngine.generate_recommendations()'s existing
      `completed_resources` parameter to avoid re-suggesting them.
    - needs_foundation_support: skills behind "too_difficult" feedback, resolved
      through the EXISTING PrerequisiteEngine (not a new DAG).
    - accelerate_skills: skills behind "too_easy" feedback.
    - deprioritize_skills: skills behind "not_relevant" feedback.
    """
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user_id).first()
    if not profile:
        raise LearnerProfileNotFoundError(f"No learner profile found for user {user_id}.")

    path_ids = [p.id for p in db.query(LearningPath.id).filter(LearningPath.profile_id == profile.id).all()]

    completed_slugs: List[str] = []
    if path_ids:
        completed_rows = (
            db.query(Course.slug)
            .join(PathItem, PathItem.course_id == Course.id)
            .join(Progress, Progress.path_item_id == PathItem.id)
            .filter(PathItem.path_id.in_(path_ids), Progress.completion_pct >= 100.0)
            .all()
        )
        completed_slugs = [row.slug for row in completed_rows]

    feedback_rows = db.query(Feedback).filter(Feedback.user_id == user_id).all()

    prereq_engine = PrerequisiteEngine(db=db)
    needs_foundation_support: List[str] = []
    accelerate_skills: List[str] = []
    deprioritize_skills: List[str] = []

    for fb in feedback_rows:
        action = _interpret_feedback(fb.rating_type)
        item = db.query(PathItem).filter(PathItem.id == fb.path_item_id).first()
        if not item or not item.course:
            continue

        target_skill_slugs = [cs.skill.slug for cs in item.course.course_skills]

        if action == "needs_foundation_support":
            for slug in target_skill_slugs:
                # Reuse the existing prerequisite DAG to find the foundation
                # skills behind the one the learner struggled with.
                chain = prereq_engine.get_prerequisite_chain(slug)
                needs_foundation_support.extend(chain if chain else [slug])
        elif action == "ready_for_faster_progression":
            accelerate_skills.extend(target_skill_slugs)
        elif action == "deprioritize_similar":
            deprioritize_skills.extend(target_skill_slugs)

    return {
        "user_id": user_id,
        # Ready to pass straight into RecommendationEngine.generate_recommendations()
        "completed_resources": sorted(set(completed_slugs)),
        "needs_foundation_support": sorted(set(needs_foundation_support)),
        "accelerate_skills": sorted(set(accelerate_skills)),
        "deprioritize_skills": sorted(set(deprioritize_skills)),
    }
