"""Qdrant vector database service for semantic search."""
import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, ScoredPoint
from app.config import settings
import uuid

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""

    def __init__(self):
        """Initialize Qdrant client with configuration."""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = "book_chunks"

    async def search(
        self,
        query_vector: List[float],
        limit: int = 7,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks in Qdrant.

        Args:
            query_vector: Query embedding vector (768 dimensions)
            limit: Maximum number of results to return (default: 7)
            score_threshold: Minimum similarity score (default: 0.7)

        Returns:
            List of matching chunks with metadata and scores

        Raises:
            Exception: If search fails
        """
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )

            chunks = []
            for point in search_result:
                chunk = {
                    "id": str(point.id),
                    "score": point.score,
                    **point.payload
                }
                chunks.append(chunk)

            logger.info(f"Found {len(chunks)} chunks above threshold {score_threshold}")
            return chunks

        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            raise

    async def upsert_points(self, points: List[Dict[str, Any]]) -> bool:
        """
        Insert or update points in Qdrant collection.

        Args:
            points: List of dictionaries containing:
                - chunk_id: Human-readable chunk identifier
                - module: Module name
                - section: Section name
                - title: Section title
                - url: URL path
                - content: Text content
                - token_count: Number of tokens
                - embedding: Vector embedding (768 dimensions)

        Returns:
            True if successful

        Raises:
            Exception: If upsert fails
        """
        try:
            point_structs = []
            for point in points:
                point_struct = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=point["embedding"],
                    payload={
                        "chunk_id": point["chunk_id"],
                        "module": point["module"],
                        "section": point["section"],
                        "title": point["title"],
                        "url": point["url"],
                        "content": point["content"],
                        "token_count": point["token_count"]
                    }
                )
                point_structs.append(point_struct)

            self.client.upsert(
                collection_name=self.collection_name,
                points=point_structs
            )

            logger.info(f"Upserted {len(point_structs)} points to Qdrant")
            return True

        except Exception as e:
            logger.error(f"Qdrant upsert failed: {e}")
            raise

    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information (count, etc.)
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": collection_info.points_count,
                "vectors_count": collection_info.vectors_count,
                "status": collection_info.status
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise
