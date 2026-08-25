"""
Custom exceptions for Recommendation Engine and Learning Path services.
"""

class RecommendationEngineError(Exception):
    """Base exception for recommendation engine errors."""
    pass

class UnknownCareerError(RecommendationEngineError):
    """Raised when the target career is not found in the database."""
    pass

class UnknownSkillError(RecommendationEngineError):
    """Raised when a requested skill is not found in the database."""
    pass

class InvalidProfileError(RecommendationEngineError):
    """Raised when learner profile data is missing or invalid."""
    pass

class NoCandidateResourcesError(RecommendationEngineError):
    """Raised when no suitable candidate learning resources can be retrieved."""
    pass


# ---------------------------------------------------------------------------
# Progress / Feedback / Adaptation module exceptions (additive — Phase 6)
# ---------------------------------------------------------------------------

class ProgressFeedbackError(Exception):
    """Base exception for the Progress/Feedback/Adaptation module."""
    pass

class PathItemNotFoundError(ProgressFeedbackError):
    """Raised when a referenced path_item_id does not exist."""
    pass

class ProgressNotFoundError(ProgressFeedbackError):
    """Raised when a progress record does not exist yet for a path item."""
    pass

class InvalidFeedbackTypeError(ProgressFeedbackError):
    """Raised when feedback rating_type is not one of the supported categories."""
    pass

class LearnerProfileNotFoundError(ProgressFeedbackError):
    """Raised when no learner profile exists for a given user_id."""
    pass
