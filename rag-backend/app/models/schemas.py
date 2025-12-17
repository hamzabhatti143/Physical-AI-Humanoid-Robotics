"""Pydantic schemas for request/response validation."""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Source(BaseModel):
    """Citation source from book content."""
    module: str = Field(..., pattern=r"^module-\d+-[\w-]+$")
    section: str
    url: str = Field(..., pattern=r"^/.*")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class ChatMessage(BaseModel):
    """Single message in conversation."""
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=10000)
    sources: Optional[List[Source]] = None
    timestamp: Optional[str] = None


class QueryRequest(BaseModel):
    """Request payload for /api/chat/query endpoint."""
    query: str = Field(..., min_length=1, max_length=2000)
    history: List[ChatMessage] = Field(default_factory=list, max_length=10)
    selected_text: Optional[str] = Field(None, max_length=5000)

    @field_validator('query')
    @classmethod
    def query_not_empty(cls, v):
        """Validate query is not empty or whitespace only."""
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()


class QueryResponse(BaseModel):
    """Response payload for /api/chat/query endpoint."""
    response: str = Field(..., min_length=1)
    sources: List[Source] = Field(default_factory=list)


class FeedbackRequest(BaseModel):
    """Request payload for /api/chat/feedback endpoint."""
    query: str = Field(..., min_length=1, max_length=2000)
    response: str = Field(..., min_length=1)
    selected_text: Optional[str] = Field(None, max_length=5000)
    rating: int = Field(..., ge=-1, le=1)
    comment: Optional[str] = Field(None, max_length=1000)
    session_id: Optional[str] = None
    sources: Optional[List[Source]] = None

    @field_validator('rating')
    @classmethod
    def rating_valid(cls, v):
        """Validate rating is 1 or -1."""
        if v not in [1, -1]:
            raise ValueError('Rating must be 1 (thumbs up) or -1 (thumbs down)')
        return v


class HealthStatus(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    services: dict
    version: str
