"""
Phase 5 API Router: LLM Conversational Assistant.

Exposes endpoints for interactive questions, recommendation explanations,
and learning path guidance grounded in verified recommendation context.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.services.assistant_service import ConversationalAssistantService
from backend.app.schemas.assistant import (
    AssistantChatRequest,
    AssistantChatResponse,
    ExplainResourceRequest
)

router = APIRouter()

_assistant_service = ConversationalAssistantService()


@router.post(
    "/assistant/chat",
    response_model=AssistantChatResponse,
    status_code=200,
    summary="Chat with the Learning Path Assistant",
    description=(
        "Answers learner questions regarding recommendations, prerequisite locks, roadmap ordering, "
        "and time management strictly grounded in deterministic backend outputs."
    ),
)
def chat_with_assistant(
    body: AssistantChatRequest,
    db: Session = Depends(get_db),
) -> AssistantChatResponse:
    """
    Main conversational assistant endpoint.
    """
    profile_dict = body.profile.model_dump()
    result = _assistant_service.generate_chat_response(
        message=body.message,
        profile_data=profile_dict,
        db=db,
        resource_slug=body.resource_slug,
        history=body.history
    )
    return AssistantChatResponse(**result)


@router.post(
    "/assistant/explain-resource",
    response_model=AssistantChatResponse,
    status_code=200,
    summary="Explain a specific recommended or locked resource",
    description="Provides an in-depth explanation of why a resource was recommended or why it is locked.",
)
def explain_resource(
    body: ExplainResourceRequest,
    db: Session = Depends(get_db),
) -> AssistantChatResponse:
    """
    Convenience endpoint to explain a specific course/resource card.
    """
    profile_dict = body.profile.model_dump()
    result = _assistant_service.generate_chat_response(
        message=f"Explain why {body.resource_slug} was recommended or if it is locked.",
        profile_data=profile_dict,
        db=db,
        resource_slug=body.resource_slug,
        history=[]
    )
    return AssistantChatResponse(**result)


@router.get(
    "/assistant/status",
    status_code=200,
    summary="Check assistant engine status",
    description="Returns whether the LLM assistant is using Gemini or deterministic fallback mode.",
)
def get_assistant_status():
    """Returns engine availability and model configuration."""
    has_api_key = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip())
    return {
        "status": "ready",
        "llm_provider": "gemini" if has_api_key else "deterministic-fallback",
        "model": settings.LLM_MODEL if has_api_key else "rule-based-engine",
        "api_key_configured": has_api_key
    }
