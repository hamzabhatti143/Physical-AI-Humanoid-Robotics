"""Setup script for Qdrant Cloud vector database."""
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config import settings


def create_collection():
    """Create Qdrant collection for book chunks."""
    try:
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )

        # Delete if exists (for clean setup)
        try:
            client.delete_collection("book_chunks")
            print("🗑️  Deleted existing collection")
        except Exception:
            pass  # Collection doesn't exist

        # Create new collection
        client.create_collection(
            collection_name="book_chunks",
            vectors_config=VectorParams(
                size=768,  # Gemini text-embedding-004 dimension
                distance=Distance.COSINE
            ),
            optimizers_config={
                "indexing_threshold": 10000
            },
            hnsw_config={
                "m": 16,
                "ef_construct": 100
            }
        )

        print("✅ Qdrant collection 'book_chunks' created successfully")
        print("   - Vector size: 768 dimensions")
        print("   - Distance metric: COSINE")
        return True

    except Exception as e:
        print(f"❌ Error creating Qdrant collection: {e}")
        return False


if __name__ == "__main__":
    create_collection()
