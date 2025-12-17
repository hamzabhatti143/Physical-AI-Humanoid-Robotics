"""Application configuration using Pydantic Settings."""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Gemini API
    gemini_api_key: str

    # Qdrant Cloud
    qdrant_url: str
    qdrant_api_key: str

    # Neon Postgres
    neon_database_url: str

    # Book Content Path
    book_content_path: str = "../physical-ai-humanoid-robotics/docs"

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
