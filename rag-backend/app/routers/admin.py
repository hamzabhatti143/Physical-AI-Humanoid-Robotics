"""Admin router for health checks and maintenance endpoints."""
from fastapi import APIRouter
from datetime import datetime
from app.models.schemas import HealthStatus

router = APIRouter()


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint.

    Returns system health status including:
    - API service availability
    - Qdrant connection status
    - Neon Postgres connection status
    - Gemini API connectivity

    TODO: Implement actual health checks for each service
    """
    return HealthStatus(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        services={
            "qdrant": "connected",  # TODO: implement actual Qdrant health check
            "postgres": "connected",  # TODO: implement actual Postgres health check
            "gemini": "connected"  # TODO: implement actual Gemini API check
        },
        version="1.0.0"
    )
