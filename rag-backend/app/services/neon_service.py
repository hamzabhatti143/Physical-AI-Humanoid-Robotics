"""Neon Postgres service for feedback storage."""
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
from app.models.database import Feedback
import json

logger = logging.getLogger(__name__)


class NeonService:
    """Service for interacting with Neon Postgres database."""

    def __init__(self):
        """Initialize Neon service with database connection."""
        self.engine = create_engine(settings.neon_database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

    async def store_feedback(
        self,
        query: str,
        response: str,
        rating: int,
        selected_text: Optional[str] = None,
        comment: Optional[str] = None,
        session_id: Optional[str] = None,
        sources: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Store user feedback in database.

        Args:
            query: Original user question
            response: Chatbot's answer
            rating: 1 (thumbs up) or -1 (thumbs down)
            selected_text: Highlighted text context (if Mode B query)
            comment: Optional written feedback
            session_id: Browser session identifier
            sources: List of citation sources

        Returns:
            Feedback ID (UUID as string)

        Raises:
            Exception: If storage fails
        """
        session = self.SessionLocal()
        try:
            # Convert sources to JSON if provided
            sources_json = json.dumps(sources) if sources else None

            feedback = Feedback(
                query=query,
                response=response,
                selected_text=selected_text,
                rating=rating,
                comment=comment,
                session_id=session_id,
                sources_json=sources_json
            )

            session.add(feedback)
            session.commit()
            session.refresh(feedback)

            feedback_id = str(feedback.id)
            logger.info(f"Stored feedback with ID: {feedback_id}")
            return feedback_id

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Failed to store feedback: {e}")
            raise
        finally:
            session.close()

    async def get_feedback_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored feedback.

        Returns:
            Dictionary with feedback counts

        Raises:
            Exception: If query fails
        """
        session = self.SessionLocal()
        try:
            total_count = session.query(Feedback).count()
            positive_count = session.query(Feedback).filter(Feedback.rating == 1).count()
            negative_count = session.query(Feedback).filter(Feedback.rating == -1).count()

            stats = {
                "total": total_count,
                "positive": positive_count,
                "negative": negative_count,
                "positive_rate": round(positive_count / total_count * 100, 2) if total_count > 0 else 0
            }

            logger.info(f"Feedback stats: {stats}")
            return stats

        except SQLAlchemyError as e:
            logger.error(f"Failed to get feedback stats: {e}")
            raise
        finally:
            session.close()
