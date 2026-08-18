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
