"""Embedding generation utilities using Gemini API."""
import asyncio
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential
import google.generativeai as genai
from app.config import settings
from app.utils.logger import logger

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text using Gemini.

    Uses text-embedding-004 model (768 dimensions).
    Includes exponential backoff for rate limiting.

    Args:
        text: Text to generate embedding for

    Returns:
        768-dimensional embedding vector

    Raises:
        Exception: If embedding generation fails after retries
    """
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise


async def batch_generate_embeddings(
    texts: List[str],
    batch_size: int = 50
) -> List[List[float]]:
    """
    Generate embeddings for multiple texts in batches.

    Processes texts in batches of 50 with 1s delays to respect rate limits.

    Args:
        texts: List of texts to generate embeddings for
        batch_size: Number of texts per batch (default: 50)

    Returns:
        List of embedding vectors (one per text)
    """
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

        # Generate embeddings for batch
        batch_embeddings = []
        for text in batch:
            embedding = await generate_embedding(text)
            batch_embeddings.append(embedding)

        embeddings.extend(batch_embeddings)

        # Rate limit protection: 1s delay between batches
        if i + batch_size < len(texts):
            await asyncio.sleep(1)

    logger.info(f"Generated {len(embeddings)} embeddings")
    return embeddings
