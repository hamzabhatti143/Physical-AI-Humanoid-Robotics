"""Text chunking utilities for semantic content segmentation."""
import re
import tiktoken
from typing import List


def chunk_markdown(
    content: str,
    max_tokens: int = 1000,
    min_tokens: int = 500
) -> List[str]:
    """
    Chunk markdown content into semantic sections.

    Uses heading-based splitting to preserve context boundaries.
    Each chunk is 500-1000 tokens.

    Args:
        content: Markdown content to chunk
        max_tokens: Maximum tokens per chunk
        min_tokens: Minimum tokens per chunk

    Returns:
        List of content chunks
    """
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer

    # Split by level-2 headings (##)
    sections = re.split(r'\n## ', content)

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for i, section in enumerate(sections):
        # Add heading prefix back (except for first section if it has no heading)
        if i > 0:
            section = "## " + section

        section_tokens = len(encoding.encode(section))

        # If section alone exceeds max_tokens, split by paragraphs
        if section_tokens > max_tokens:
            paragraphs = section.split('\n\n')
            for para in paragraphs:
                para_tokens = len(encoding.encode(para))

                if current_tokens + para_tokens > max_tokens:
                    if current_tokens >= min_tokens:
                        chunks.append(current_chunk.strip())
                        current_chunk = para
                        current_tokens = para_tokens
                    else:
                        # Current chunk too small, force combine even if exceeds max
                        current_chunk += "\n\n" + para
                        current_tokens += para_tokens
                else:
                    if current_chunk:
                        current_chunk += "\n\n" + para
                    else:
                        current_chunk = para
                    current_tokens += para_tokens
        else:
            # Section fits within limits
            if current_tokens + section_tokens > max_tokens:
                if current_tokens >= min_tokens:
                    chunks.append(current_chunk.strip())
                    current_chunk = section
                    current_tokens = section_tokens
                else:
                    # Combine even if exceeds max
                    current_chunk += "\n\n" + section
                    current_tokens += section_tokens
            else:
                if current_chunk:
                    current_chunk += "\n\n" + section
                else:
                    current_chunk = section
                current_tokens += section_tokens

    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def count_tokens(text: str) -> int:
    """
    Count tokens in text using tiktoken.

    Args:
        text: Text to count tokens for

    Returns:
        Number of tokens
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
