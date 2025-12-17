"""Indexing script to process book content and upload to Qdrant."""
import sys
import os
import asyncio
from pathlib import Path
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import frontmatter
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from app.config import settings
from app.utils.chunking import chunk_markdown, count_tokens
from app.utils.embedding import batch_generate_embeddings
from app.utils.logger import logger


def generate_url_path(file_path: str, docs_root: str) -> str:
    """
    Generate URL path from file path.

    Example: docs/module-1-ros2/week-3-fundamentals.md -> /module-1-ros2/week-3-fundamentals

    Args:
        file_path: Full file path
        docs_root: Root docs directory

    Returns:
        URL path string
    """
    rel_path = Path(file_path).relative_to(docs_root)
    url_path = "/" + str(rel_path.with_suffix("")).replace("\\", "/")
    return url_path


def extract_module_section(file_path: str, docs_root: str) -> tuple:
    """
    Extract module and section from file path.

    Example: docs/module-1-ros2/week-3-fundamentals.md
             -> module: "module-1-ros2", section: "week-3-fundamentals"

    Args:
        file_path: Full file path
        docs_root: Root docs directory

    Returns:
        Tuple of (module, section)
    """
    rel_path = Path(file_path).relative_to(docs_root)
    parts = rel_path.parts

    if len(parts) >= 2:
        module = parts[0]
        section = rel_path.stem
    elif len(parts) == 1:
        module = "root"
        section = rel_path.stem
    else:
        module = "unknown"
        section = "unknown"

    return module, section


async def index_book_content():
    """Main indexing function to process all markdown files."""
    # Get docs directory
    docs_path = Path(settings.book_content_path)
    if not docs_path.exists():
        logger.error(f"Docs directory not found: {docs_path}")
        return

    logger.info(f"Starting indexing from: {docs_path}")

    # Find all markdown files
    md_files = list(docs_path.rglob("*.md"))
    logger.info(f"Found {len(md_files)} markdown files")

    # Connect to Qdrant
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )

    all_chunks_data = []
    chunk_counter = 0

    # Process each file
    for file_path in md_files:
        logger.info(f"Processing: {file_path.name}")

        try:
            # Parse frontmatter and content
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            metadata = post.metadata
            content = post.content

            if not content.strip():
                logger.warning(f"Skipping empty file: {file_path.name}")
                continue

            # Extract module and section
            module, section = extract_module_section(str(file_path), str(docs_path))

            # Get title from frontmatter or use filename
            title = metadata.get('title', file_path.stem.replace('-', ' ').title())

            # Generate URL path
            url = generate_url_path(str(file_path), str(docs_path))

            # Chunk content
            chunks = chunk_markdown(content)
            logger.info(f"  Created {len(chunks)} chunks")

            # Prepare chunk data
            for i, chunk_content in enumerate(chunks):
                chunk_counter += 1
                chunk_id = f"m{module.split('-')[1] if '-' in module else '0'}_w{section.split('-')[1] if '-' in section and 'week' in section else '0'}_c{i+1}"

                all_chunks_data.append({
                    'chunk_id': chunk_id,
                    'module': module,
                    'section': section,
                    'title': title,
                    'url': url,
                    'content': chunk_content,
                    'token_count': count_tokens(chunk_content)
                })

        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            continue

    logger.info(f"Total chunks prepared: {len(all_chunks_data)}")

    # Generate embeddings in batches
    logger.info("Generating embeddings...")
    chunk_texts = [chunk['content'] for chunk in all_chunks_data]
    embeddings = await batch_generate_embeddings(chunk_texts, batch_size=50)

    logger.info(f"Generated {len(embeddings)} embeddings")

    # Upload to Qdrant
    logger.info("Uploading to Qdrant...")
    points = []
    for chunk_data, embedding in zip(all_chunks_data, embeddings):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                'chunk_id': chunk_data['chunk_id'],
                'module': chunk_data['module'],
                'section': chunk_data['section'],
                'title': chunk_data['title'],
                'url': chunk_data['url'],
                'content': chunk_data['content'],
                'token_count': chunk_data['token_count']
            }
        )
        points.append(point)

    # Upload in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        client.upsert(
            collection_name="book_chunks",
            points=batch
        )
        logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")

    logger.info(f"✅ Indexing complete! Indexed {len(points)} chunks")


if __name__ == "__main__":
    asyncio.run(index_book_content())
