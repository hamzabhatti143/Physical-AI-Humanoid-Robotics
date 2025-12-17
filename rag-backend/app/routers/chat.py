"""Chat API endpoints for query and feedback."""
import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, FeedbackRequest
from app.services.rag_service import RAGService
from app.services.neon_service import NeonService
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def chat_query(request: QueryRequest):
    """
    Process user query and return RAG response with citations.

    Args:
        request: QueryRequest with query, history, and optional selected_text

    Returns:
        QueryResponse with generated answer and sources

    Raises:
        HTTPException: 400 for validation errors, 429 for rate limits, 500 for internal errors
    """
    try:
        start_time = datetime.utcnow()

        # Initialize RAG service
        rag_service = RAGService()

        # Process query
        response = await rag_service.process_query(
            query=request.query,
            history=request.history,
            selected_text=request.selected_text
        )

        # Log metrics
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        logger.info(
            f"Query processed in {processing_time:.2f}s | "
            f"Sources: {len(response.sources)} | "
            f"Query length: {len(request.query)} chars"
        )

        return response

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Query processing failed: {e}")

        # Check for API quota errors
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(
                status_code=429,
                detail="API rate limit exceeded. Please wait a moment and try again."
            )

        # Generic error
        raise HTTPException(
            status_code=500,
            detail="Failed to process query. Please try again."
        )


@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback on a chatbot response.

    Args:
        request: FeedbackRequest with query, response, rating, and optional comment

    Returns:
        Success message with feedback ID

    Raises:
        HTTPException: 400 for validation errors, 500 for database errors
    """
    try:
        # Initialize Neon service
        neon_service = NeonService()

        # Store feedback
        feedback_id = await neon_service.store_feedback(
            query=request.query,
            response=request.response,
            rating=request.rating,
            selected_text=request.selected_text,
            comment=request.comment,
            session_id=request.session_id,
            sources=[source.dict() for source in request.sources] if request.sources else None
        )

        logger.info(f"Feedback stored with ID: {feedback_id} | Rating: {request.rating}")

        return {
            "message": "Thank you for your feedback!",
            "feedback_id": feedback_id
        }

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to store feedback: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to store feedback. Please try again."
        )
