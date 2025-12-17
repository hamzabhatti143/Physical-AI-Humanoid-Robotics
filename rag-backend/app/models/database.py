"""SQLAlchemy database models."""
from sqlalchemy import Column, String, Text, Integer, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Feedback(Base):
    """Feedback table for storing user feedback on chatbot responses."""
    __tablename__ = 'feedback'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())
    session_id = Column(String(255), nullable=True)
    sources_json = Column(JSONB, nullable=True)

    __table_args__ = (
        CheckConstraint('rating IN (1, -1)', name='rating_check'),
        CheckConstraint('LENGTH(query) <= 2000', name='query_length_check'),
        CheckConstraint(
            'comment IS NULL OR LENGTH(comment) <= 1000',
            name='comment_length_check'
        ),
    )
