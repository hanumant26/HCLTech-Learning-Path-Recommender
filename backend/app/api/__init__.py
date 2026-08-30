"""
API routers module for FastAPI application.
Exports all router objects for registration in main.py.
"""
from backend.app.api.careers import router as careers_router
from backend.app.api.skills import router as skills_router
from backend.app.api.learner import router as learner_router
from backend.app.api.recommendations import router as recommendations_router
from backend.app.api.learning_path import router as learning_path_router
from backend.app.api.assistant import router as assistant_router

# Progress/Feedback/Adaptation module (additive)
from backend.app.api.progress import router as progress_router
from backend.app.api.feedback import router as feedback_router
from backend.app.api.path_management import router as path_management_router

__all__ = [
    "careers_router",
    "skills_router",
    "learner_router",
    "recommendations_router",
    "learning_path_router",
    "assistant_router",
    "progress_router",
    "feedback_router",
    "path_management_router",
]
