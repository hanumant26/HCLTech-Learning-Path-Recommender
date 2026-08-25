"""
FastAPI application entry point.

Phase 4 additions:
  - CORSMiddleware (allow all origins in development)
  - Five /api/* routers (careers, skills, learner, recommendations, learning-path)
  - Global exception handlers mapping service exceptions to HTTP JSON responses
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.database import init_db
from backend.app.services.exceptions import (
    InvalidProfileError,
    UnknownCareerError,
    NoCandidateResourcesError,
    RecommendationEngineError,
    PathItemNotFoundError,
    ProgressNotFoundError,
    InvalidFeedbackTypeError,
    LearnerProfileNotFoundError,
)
from backend.app.api import (
    careers_router,
    skills_router,
    learner_router,
    recommendations_router,
    learning_path_router,
    progress_router,
    feedback_router,
    path_management_router,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=(
        "AI-Powered Personalized Learning Path Recommender — Phase 4 API. "
        "Exposes the recommendation engine, skill gap analysis, and learning path "
        "generation through a clean REST interface for the React frontend."
    ),
)

# ---------------------------------------------------------------------------
# CORS — allow all origins in development; tighten via env var in production
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    """Ensure database tables are initialized on startup."""
    init_db()

# ---------------------------------------------------------------------------
# Global exception handlers — map service exceptions to HTTP JSON responses
# ---------------------------------------------------------------------------

@app.exception_handler(InvalidProfileError)
async def invalid_profile_handler(request, exc: InvalidProfileError):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc), "error_type": "invalid_profile"},
    )


@app.exception_handler(UnknownCareerError)
async def unknown_career_handler(request, exc: UnknownCareerError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "error_type": "career_not_found"},
    )


@app.exception_handler(NoCandidateResourcesError)
async def no_candidates_handler(request, exc: NoCandidateResourcesError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "error_type": "no_candidates"},
    )


@app.exception_handler(RecommendationEngineError)
async def recommendation_engine_handler(request, exc: RecommendationEngineError):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "error_type": "recommendation_engine_error"},
    )


# --- Progress/Feedback/Adaptation module exception handlers (additive) -----

@app.exception_handler(PathItemNotFoundError)
async def path_item_not_found_handler(request, exc: PathItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "error_type": "path_item_not_found"},
    )


@app.exception_handler(ProgressNotFoundError)
async def progress_not_found_handler(request, exc: ProgressNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "error_type": "progress_not_found"},
    )


@app.exception_handler(InvalidFeedbackTypeError)
async def invalid_feedback_type_handler(request, exc: InvalidFeedbackTypeError):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc), "error_type": "invalid_feedback_type"},
    )


@app.exception_handler(LearnerProfileNotFoundError)
async def learner_profile_not_found_handler(request, exc: LearnerProfileNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "error_type": "learner_profile_not_found"},
    )

# ---------------------------------------------------------------------------
# Routers — all mounted under /api prefix
# ---------------------------------------------------------------------------

app.include_router(careers_router,         prefix="/api", tags=["Careers"])
app.include_router(skills_router,          prefix="/api", tags=["Skills"])
app.include_router(learner_router,         prefix="/api", tags=["Learner"])
app.include_router(recommendations_router, prefix="/api", tags=["Recommendations"])
app.include_router(learning_path_router,   prefix="/api", tags=["Learning Path"])
app.include_router(progress_router,        prefix="/api", tags=["Progress"])
app.include_router(feedback_router,        prefix="/api", tags=["Feedback"])
app.include_router(path_management_router, prefix="/api", tags=["Path Management"])

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
