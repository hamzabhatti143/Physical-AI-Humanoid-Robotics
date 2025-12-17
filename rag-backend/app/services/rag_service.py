"""RAG service for query processing and response generation."""
import logging
from typing import List, Optional, Dict, Any
from app.services.gemini_service import GeminiService
from app.services.qdrant_service import QdrantService
from app.models.schemas import ChatMessage, Source, QueryResponse

logger = logging.getLogger(__name__)


class RAGService:
    """Service for orchestrating RAG pipeline."""

    def __init__(self):
        """Initialize RAG service with dependencies."""
        self.gemini = GeminiService()
        self.qdrant = QdrantService()

    async def process_query(
        self,
        query: str,
        history: Optional[List[ChatMessage]] = None,
        selected_text: Optional[str] = None
    ) -> QueryResponse:
        """
        Process user query through RAG pipeline.

        Args:
            query: User's question
            history: Previous conversation messages (max 10)
            selected_text: Highlighted text from book (Mode B)

        Returns:
            QueryResponse with generated answer and citations

        Raises:
            Exception: If processing fails
        """
        try:
            # Step 1: Generate query embedding
            logger.info(f"Processing query: {query[:100]}...")
            query_embedding = await self.gemini.generate_embedding(query)

            # Step 2: Search Qdrant for similar chunks
            # Reduce limit if selected_text is provided (Mode B)
            search_limit = 3 if selected_text else 7
            chunks = await self.qdrant.search(
                query_vector=query_embedding,
                limit=search_limit,
                score_threshold=0.5
            )

            # Step 3: Handle no results
            if not chunks:
                logger.warning("No relevant chunks found for query")
                return QueryResponse(
                    response="I don't have information about that in the book. Please try asking about topics covered in the Physical AI & Humanoid Robotics modules.",
                    sources=[]
                )

            # Step 4: Build context and prompt
            context = self._build_context(chunks, history, selected_text)
            prompt = self._build_prompt(query, context, selected_text)

            # Step 5: Generate response
            response_text = await self.gemini.generate_response(prompt)

            # Step 6: Extract citations
            sources = self._extract_citations(chunks)

            logger.info(f"Generated response with {len(sources)} citations")
            return QueryResponse(
                response=response_text,
                sources=sources
            )

        except Exception as e:
            logger.error(f"RAG pipeline failed: {e}")
            raise

    def _build_context(
        self,
        chunks: List[Dict[str, Any]],
        history: Optional[List[ChatMessage]],
        selected_text: Optional[str]
    ) -> str:
        """
        Build context from retrieved chunks and conversation history.

        Args:
            chunks: Retrieved chunks from Qdrant
            history: Previous conversation messages
            selected_text: Highlighted text (if Mode B)

        Returns:
            Formatted context string
        """
        context_parts = []

        # Add selected text first (Mode B takes priority)
        if selected_text:
            context_parts.append(f"Selected Text Context:\n{selected_text}\n")

        # Add retrieved chunks
        context_parts.append("Relevant Book Content:")
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"\n[Source {i}: {chunk['module']}/{chunk['section']}]\n"
                f"{chunk['content']}"
            )

        # Add conversation history (keep last 10 messages)
        if history:
            recent_history = history[-10:] if len(history) > 10 else history
            context_parts.append("\n\nConversation History:")
            for msg in recent_history:
                role = "User" if msg.role == "user" else "Assistant"
                context_parts.append(f"{role}: {msg.content}")

        return "\n".join(context_parts)

    def _build_prompt(
        self,
        query: str,
        context: str,
        selected_text: Optional[str]
    ) -> str:
        """
        Build prompt for Gemini with instructions and context.

        Args:
            query: User's question
            context: Formatted context with chunks and history
            selected_text: Highlighted text (if Mode B)

        Returns:
            Complete prompt string
        """
        system_instructions = """You are a helpful assistant for the Physical AI & Humanoid Robotics textbook.

Your task is to answer questions based ONLY on the provided context from the book. Follow these guidelines:

1. Use the context to provide accurate, helpful answers
2. Always cite the specific module and section where you found the information
3. If the context doesn't contain the answer, say "I don't have information about that in the book"
4. Keep answers concise but informative (2-4 paragraphs)
5. Use technical terms from the book but explain them clearly
6. If selected text is provided, focus your answer on that specific content
"""

        if selected_text:
            system_instructions += "\n7. The user has highlighted specific text - prioritize explaining that content in your response\n"

        prompt = f"""{system_instructions}

Context:
{context}

User Question: {query}

Please provide a helpful answer based on the context above."""

        return prompt

    def _extract_citations(self, chunks: List[Dict[str, Any]]) -> List[Source]:
        """
        Extract citation sources from chunks.

        Args:
            chunks: Retrieved chunks from Qdrant

        Returns:
            List of Source objects for citations
        """
        sources = []
        seen_urls = set()

        for chunk in chunks:
            url = chunk.get("url")
            # Avoid duplicate sources
            if url and url not in seen_urls:
                source = Source(
                    module=chunk.get("module", ""),
                    section=chunk.get("section", ""),
                    url=url,
                    relevance_score=chunk.get("score")
                )
                sources.append(source)
                seen_urls.add(url)

        return sources