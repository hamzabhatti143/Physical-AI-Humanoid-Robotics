"""Gemini API service for embeddings and text generation."""
import logging
from typing import List
import google.generativeai as genai
from google.api_core import retry as google_retry
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API."""

    def __init__(self):
        """Initialize Gemini service with API key."""
        genai.configure(api_key=settings.gemini_api_key)
        self.embedding_model = "models/text-embedding-004"
        self.generation_model = "models/gemini-2.0-flash-001"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to generate embedding for

        Returns:
            List of floats representing the embedding (768 dimensions)

        Raises:
            Exception: If embedding generation fails after retries
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_query"
            )
            embedding = result['embedding']
            logger.info(f"Generated embedding for text (length: {len(text)} chars)")
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def batch_generate_embeddings(
        self,
        texts: List[str],
        task_type: str = "retrieval_document"
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to generate embeddings for
            task_type: Type of task ("retrieval_document" for indexing, "retrieval_query" for queries)

        Returns:
            List of embeddings (each is a list of 768 floats)

        Raises:
            Exception: If batch embedding generation fails after retries
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=texts,
                task_type=task_type
            )
            embeddings = result['embedding']
            logger.info(f"Generated {len(embeddings)} embeddings for batch")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate_response(self, prompt: str) -> str:
        """
        Generate text response using Gemini.

        Args:
            prompt: Prompt to generate response for (includes context and question)

        Returns:
            Generated text response

        Raises:
            Exception: If generation fails after retries
        """
        try:
            model = genai.GenerativeModel(self.generation_model)
            response = model.generate_content(prompt)

            if not response.text:
                logger.warning("Empty response from Gemini")
                return "I couldn't generate a response. Please try again."

            logger.info(f"Generated response (length: {len(response.text)} chars)")
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise
