"""
Phase 5 API schemas for LLM Conversational Assistant.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.schemas.api_responses import LearnerProfileRequest


class ChatMessage(BaseModel):
    """A single turn in a conversational dialogue."""
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str = Field(..., description="Text content of the message")


class AssistantChatRequest(BaseModel):
    """
    Request body for POST /api/assistant/chat.
    Accepts learner's current query, learner profile, optional focused resource, and chat history.
    """
    message: str = Field(
        ...,
        description="The learner's natural language query or question",
        examples=["Why was Machine Learning Specialization recommended?", "Why is this course locked?"]
    )
    profile: LearnerProfileRequest = Field(
        ...,
        description="Current learner profile containing target career, skills, and weekly hours"
    )
    resource_slug: Optional[str] = Field(
        default=None,
        description="Optional resource slug if the question focuses on a specific course/project"
    )
    history: Optional[List[ChatMessage]] = Field(
        default_factory=list,
        description="Previous conversation turns for conversational continuity"
    )


class ExplainResourceRequest(BaseModel):
    """
    Convenience request for POST /api/assistant/explain-resource.
    """
    resource_slug: str = Field(
        ...,
        description="Resource slug to explain (e.g. 'machine-learning-specialization')"
    )
    profile: LearnerProfileRequest = Field(
        ...,
        description="Current learner profile"
    )


class AssistantChatResponse(BaseModel):
    """
    Response body returned by the conversational assistant.
    Contains grounded natural language answer, detected intent, referenced resources, and grounding metadata.
    """
    answer: str = Field(
        ...,
        description="Grounded explanation or guidance formatted in Markdown"
    )
    intent: str = Field(
        ...,
        description="Recognized question category (e.g. 'why_recommended', 'why_locked', 'what_next', 'skip_prerequisite', 'time_budget', 'general_guidance')"
    )
    referenced_resources: List[str] = Field(
        default_factory=list,
        description="Slugs of courses or milestones referenced in the answer"
    )
    grounding_summary: Dict[str, Any] = Field(
        default_factory=dict,
        description="Deterministic context and metrics used to formulate and ground the response"
    )
    engine: str = Field(
        ...,
        description="Generation engine used: 'gemini' or 'deterministic-fallback'"
    )
