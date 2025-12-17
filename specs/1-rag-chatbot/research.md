# Research: RAG Chatbot Technology Decisions and Patterns

**Feature**: 1-rag-chatbot
**Date**: 2025-12-15
**Purpose**: Document technology research, decisions, and implementation patterns for Phase 0

## Research Questions & Findings

### 1. Gemini API Integration Patterns

#### Question
What is the recommended way to handle Gemini rate limits, structure RAG prompts, and perform batch embedding generation?

#### Findings

**Rate Limiting**:
- Gemini API free tier: 15 RPM (requests per minute), 1 million TPM (tokens per minute), 1500 RPD (requests per day)
- Paid tier (Pay-as-you-go): 360 RPM, 4 million TPM
- **Recommendation**: Implement exponential backoff with `tenacity` library:
  ```python
  from tenacity import retry, stop_after_attempt, wait_exponential
  from google.api_core import retry as google_retry

  @retry(
      stop=stop_after_attempt(3),
      wait=wait_exponential(multiplier=1, min=2, max=10),
      reraise=True
  )
  async def generate_embedding(text: str):
      # Gemini API call
      pass
  ```

**RAG Prompt Structure**:
- Use system instructions to define chatbot role and constraints
- Include retrieved context at the beginning of user prompt
- Limit context to top 5-7 chunks (avoid token limits)
- Example prompt template:
  ```text
  You are a helpful assistant for the Physical AI & Humanoid Robotics textbook.
  Use the following context from the book to answer the question.
  Always cite the specific module and section. If the context doesn't contain
  the answer, say "I don't have information about that in the book."

  Context:
  [Chunk 1: module-1-ros2/week-3-fundamentals]
  {content}

  [Chunk 2: module-3-nvidia-isaac/week-8-intro]
  {content}

  Conversation History:
  User: {previous_question}
  Assistant: {previous_answer}

  Current Question: {user_query}
  ```

**Batch Embedding Generation**:
- Use `embed_content` API with batch support (up to 100 texts per request for embeddings)
- For indexing 500-1000 chunks: batch in groups of 50, add 1s delay between batches
- Implementation:
  ```python
  import asyncio
  from google.generativeai import embed_content

  async def batch_generate_embeddings(texts: List[str], batch_size=50):
      embeddings = []
      for i in range(0, len(texts), batch_size):
          batch = texts[i:i+batch_size]
          result = await embed_content(
              model="models/text-embedding-004",
              content=batch,
              task_type="retrieval_document"
          )
          embeddings.extend(result.embeddings)
          if i + batch_size < len(texts):
              await asyncio.sleep(1)  # Rate limit protection
      return embeddings
  ```

**Decision**: Use `google-generativeai` Python SDK with exponential backoff for rate limiting. Structure prompts with context-first format. Batch embeddings in groups of 50 with 1s delays.

**Rationale**: Official SDK provides best compatibility and error handling. Context-first prompts improve grounding. Batching reduces API calls while staying within rate limits.

---

### 2. Qdrant Cloud Setup

#### Question
How to structure collections for optimal search performance, choose distance metrics, and handle re-indexing?

#### Findings

**Collection Structure**:
- Create single collection named `book_chunks` with 768-dimensional vectors (text-embedding-004)
- Payload schema:
  ```json
  {
    "chunk_id": "m1_w3_c1",
    "module": "module-1-ros2",
    "section": "week-3-fundamentals",
    "title": "ROS 2 Architecture",
    "url": "/module-1-ros2/week-3-fundamentals",
    "content": "ROS 2 uses a Data Distribution Service...",
    "token_count": 756
  }
  ```
- Use UUIDs for point IDs, chunk_id as payload field for human readability
- **Recommendation**:
  ```python
  from qdrant_client import QdrantClient
  from qdrant_client.models import Distance, VectorParams

  client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

  client.create_collection(
      collection_name="book_chunks",
      vectors_config=VectorParams(size=768, distance=Distance.COSINE),
      optimizers_config={
          "indexing_threshold": 10000  # Build index after 10k points
      }
  )
  ```

**Distance Metric**:
- Gemini embeddings are normalized, so COSINE and DOT product are equivalent
- **Decision**: Use **COSINE** distance for semantic similarity
- Rationale: More intuitive (1.0 = identical, 0.0 = orthogonal), standard for text embeddings

**Re-indexing Strategy**:
- **Option 1**: Delete and recreate collection (simple, full refresh)
- **Option 2**: Upsert points (preserve existing, update changed)
- **Decision**: Use delete + recreate for MVP (simpler, ensures consistency)
- Implementation:
  ```python
  def refresh_index():
      # Delete old collection
      try:
          client.delete_collection("book_chunks")
      except Exception:
          pass  # Collection doesn't exist

      # Recreate collection
      client.create_collection(...)

      # Re-index all chunks
      chunks = parse_all_markdown_files()
      embeddings = batch_generate_embeddings([c.content for c in chunks])

      # Upload to Qdrant
      client.upload_points(
          collection_name="book_chunks",
          points=[
              {
                  "id": str(uuid.uuid4()),
                  "vector": embedding,
                  "payload": chunk.to_dict()
              }
              for chunk, embedding in zip(chunks, embeddings)
          ]
      )
  ```

**Search Optimization**:
- Use `query_points` with `limit=7` for top-7 chunks
- Add score threshold (e.g., `score_threshold=0.7`) to filter low-relevance results
- Enable HNSW indexing for fast approximate search (default in Qdrant)

**Decision**: Single collection with COSINE distance, delete+recreate for re-indexing, top-7 search with 0.7 score threshold.

**Rationale**: Simple architecture, predictable performance, adequate for 500-1000 chunks. Can optimize later with incremental updates if needed.

---

### 3. Markdown Parsing for Book Content

#### Question
How to extract frontmatter, perform semantic chunking, and generate correct URL paths from Docusaurus markdown?

#### Findings

**Frontmatter Extraction**:
- Docusaurus uses YAML frontmatter (between `---` delimiters)
- Use `python-frontmatter` library for parsing
- Example:
  ```python
  import frontmatter

  with open("docs/module-1-ros2/week-3-fundamentals.md") as f:
      post = frontmatter.load(f)
      metadata = post.metadata  # dict: {title, sidebar_position, ...}
      content = post.content     # markdown body
  ```

**Semantic Chunking Strategy**:
- **Requirement**: 500-1000 tokens per chunk, preserve context boundaries
- **Approach**: Split by heading hierarchy, respect paragraph boundaries
- Use `tiktoken` for token counting (same tokenizer as Gemini)
- Implementation:
  ```python
  import tiktoken
  import re

  def chunk_markdown(content: str, max_tokens=1000, min_tokens=500):
      encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer

      # Split by level-2 headings (##)
      sections = re.split(r'\n## ', content)

      chunks = []
      current_chunk = ""
      current_tokens = 0

      for section in sections:
          section_tokens = len(encoding.encode(section))

          if current_tokens + section_tokens > max_tokens:
              if current_tokens >= min_tokens:
                  chunks.append(current_chunk)
                  current_chunk = section
                  current_tokens = section_tokens
              else:
                  # Current chunk too small, combine
                  current_chunk += "\n## " + section
                  current_tokens += section_tokens
          else:
              current_chunk += "\n## " + section
              current_tokens += section_tokens

      if current_chunk:
          chunks.append(current_chunk)

      return chunks
  ```

**URL Path Generation**:
- Docusaurus URLs follow pattern: `/{folder}/{filename}`
- Example: `docs/module-1-ros2/week-3-fundamentals.md` → `/module-1-ros2/week-3-fundamentals`
- Implementation:
  ```python
  from pathlib import Path

  def generate_url_path(file_path: str, docs_root: str) -> str:
      rel_path = Path(file_path).relative_to(docs_root)
      # Remove .md extension, convert to URL path
      url_path = "/" + str(rel_path.with_suffix("")).replace("\\", "/")
      return url_path
  ```

**Module/Section Extraction**:
- Parse from file path: `docs/{module}/{section}.md`
- Example: `docs/module-1-ros2/week-3-fundamentals.md`
  - module: `module-1-ros2`
  - section: `week-3-fundamentals`

**Decision**: Use `python-frontmatter` for metadata, `tiktoken` for token counting, heading-based semantic chunking (500-1000 tokens).

**Rationale**: Preserves semantic boundaries (headings), accurate token counting, standard libraries.

**Alternatives Considered**:
- Fixed character-based chunking: Rejected (breaks semantic boundaries, poor context quality)
- LangChain RecursiveCharacterTextSplitter: Rejected (overkill, prefer simple custom solution)

---

### 4. Docusaurus Theme Integration

#### Question
How to integrate chat components without breaking Docusaurus updates, access customFields, and ensure UI compatibility?

#### Findings

**Theme Swizzling vs. Root Wrapper**:
- **Swizzling**: Copy Docusaurus component to `src/theme/` and modify
  - Pros: Full control
  - Cons: Breaks on Docusaurus updates, requires manual merging
- **Root Wrapper**: Wrap entire app with custom component
  - Pros: Non-invasive, survives updates
  - Cons: Limited to app-level integration
- **Decision**: Use **Root wrapper** (`src/theme/Root.js`)
- Implementation:
  ```jsx
  // src/theme/Root.js
  import React from 'react';
  import ChatWidget from '../components/chat/ChatWidget';

  export default function Root({children}) {
    return (
      <>
        {children}
        <ChatWidget />
      </>
    );
  }
  ```

**Accessing customFields**:
- Define in `docusaurus.config.js`:
  ```js
  module.exports = {
    // ...
    customFields: {
      ragApiUrl: process.env.RAG_API_URL || 'http://localhost:8000'
    }
  };
  ```
- Access in React components:
  ```jsx
  import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

  function ChatWidget() {
    const {siteConfig} = useDocusaurusContext();
    const apiUrl = siteConfig.customFields.ragApiUrl;
    // Use apiUrl for axios requests
  }
  ```

**CSS Scoping**:
- Use CSS Modules for component styles to avoid global conflicts
- Example: `chat.css` → `chat.module.css`
  ```jsx
  import styles from './chat.module.css';

  <div className={styles.chatContainer}>
    {/* content */}
  </div>
  ```

**Responsive Design**:
- Test breakpoints: mobile (<768px), tablet (768-1024px), desktop (>1024px)
- Use Docusaurus CSS variables for consistency:
  ```css
  .chat-container {
    background: var(--ifm-background-color);
    color: var(--ifm-font-color-base);
    border: 1px solid var(--ifm-color-emphasis-300);
  }
  ```

**Decision**: Use Root wrapper for chat integration, CSS modules for styling, Docusaurus CSS variables for theming.

**Rationale**: Non-invasive approach, survives Docusaurus updates, maintains theme consistency.

**Alternatives Considered**:
- Swizzling DocRoot: Rejected (too invasive, breaks updates)
- Standalone chat page: Rejected (poor UX, violates constitution requirement)

---

### 5. Text Selection Detection in React

#### Question
What's the most reliable method for detecting text selection, positioning tooltips, and preserving selection state?

#### Findings

**Selection Detection**:
- Use `window.getSelection()` API (browser-native)
- Listen to `mouseup` and `touchend` events on document
- Filter out empty selections
- Implementation:
  ```jsx
  import React, { useEffect, useState } from 'react';

  function TextSelectionHandler({ onTextSelected }) {
    const [selection, setSelection] = useState(null);

    useEffect(() => {
      const handleSelection = () => {
        const sel = window.getSelection();
        const text = sel.toString().trim();

        if (text.length > 0) {
          const range = sel.getRangeAt(0);
          const rect = range.getBoundingClientRect();

          setSelection({
            text,
            rect: {
              top: rect.top,
              left: rect.left + rect.width / 2,
              bottom: rect.bottom
            }
          });
        } else {
          setSelection(null);
        }
      };

      document.addEventListener('mouseup', handleSelection);
      document.addEventListener('touchend', handleSelection);

      return () => {
        document.removeEventListener('mouseup', handleSelection);
        document.removeEventListener('touchend', handleSelection);
      };
    }, []);

    useEffect(() => {
      if (selection) {
        onTextSelected(selection.text);
      }
    }, [selection, onTextSelected]);

    return selection ? (
      <div
        style={{
          position: 'fixed',
          top: selection.rect.bottom + 5,
          left: selection.rect.left,
          transform: 'translateX(-50%)'
        }}
      >
        <button onClick={() => handleAskAboutText(selection.text)}>
          Ask about this text
        </button>
      </div>
    ) : null;
  }
  ```

**Cross-Browser Compatibility**:
- `window.getSelection()` supported in all modern browsers (Chrome, Firefox, Safari, Edge)
- Use `getBoundingClientRect()` for positioning (reliable across browsers)
- **Issue**: Safari on iOS requires user interaction to modify selection
- **Workaround**: Store selected text, allow user to open chat manually

**Preserving Selection State**:
- When chat opens, selection is lost (focus moves to input)
- **Solution**: Store selected text in component state before opening chat
- Pass to chat as `initialSelectedText` prop
- Display in chat UI: "Asking about: [truncated text]"

**Decision**: Use `window.getSelection()` with mouseup/touchend listeners, display floating tooltip, store text in state before opening chat.

**Rationale**: Browser-native API, cross-browser compatible, simple implementation.

**Alternatives Considered**:
- `Selection` API with Range: Rejected (same as getSelection, more complex)
- Third-party library (react-text-selection): Rejected (unnecessary dependency)

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Backend Framework | FastAPI | 0.109.0 | Async support, auto OpenAPI docs, Pydantic validation |
| Embeddings & Generation | Gemini API | text-embedding-004 (768d), gemini-1.5-flash | Unified platform, cost-effective, high quality |
| Vector Database | Qdrant Cloud | Free tier | Managed service, 1GB free, <200ms search latency |
| Relational Database | Neon Postgres | Serverless | Auto-scaling, free tier, standard SQL |
| Markdown Parsing | python-frontmatter | 1.0.0 | Standard for YAML frontmatter extraction |
| Token Counting | tiktoken | 0.5.2 | Accurate token counting (same as GPT models) |
| HTTP Client (Backend) | httpx | 0.26.0 | Async support, modern API |
| ORM | SQLAlchemy | 2.0.25 | Industry standard, async support |
| Retry Logic | tenacity | 8.2.3 | Exponential backoff, flexible configuration |
| Frontend Framework | React | 18.x (Docusaurus) | Required by Docusaurus |
| HTTP Client (Frontend) | axios | 1.6.0 | Simple API, interceptor support, browser compatible |
| Styling | CSS Modules | Built-in | Scoped styles, no global conflicts |

## Implementation Patterns

### Pattern 1: Environment Configuration

**Use Pydantic Settings for type-safe config**:
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    neon_database_url: str
    book_content_path: str = "../physical-ai-humanoid-robotics/docs"
    allowed_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
```

**Benefits**: Type validation, IDE autocomplete, clear documentation.

---

### Pattern 2: Service Layer Architecture

**Separate concerns: routers → services → external APIs**:
```python
# app/routers/chat.py
from app.services.rag_service import RAGService

@router.post("/query")
async def chat_query(request: QueryRequest):
    rag_service = RAGService()
    response = await rag_service.process_query(
        query=request.query,
        history=request.history,
        selected_text=request.selected_text
    )
    return response

# app/services/rag_service.py
class RAGService:
    def __init__(self):
        self.gemini = GeminiService()
        self.qdrant = QdrantService()

    async def process_query(self, query, history, selected_text):
        # Orchestrate RAG pipeline
        embedding = await self.gemini.generate_embedding(query)
        chunks = await self.qdrant.search(embedding, limit=7)
        context = self._build_context(chunks, history, selected_text)
        response = await self.gemini.generate_response(context)
        citations = self._extract_citations(chunks)
        return QueryResponse(response=response, sources=citations)
```

**Benefits**: Testable (mock services), maintainable (clear responsibilities), reusable (services can be used by multiple routers).

---

### Pattern 3: Error Handling with Context

**Wrap external API calls with informative errors**:
```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def generate_embedding(text: str):
    try:
        response = await gemini_client.embed_content(
            model="models/text-embedding-004",
            content=text
        )
        return response.embedding
    except google.api_core.exceptions.ResourceExhausted as e:
        logger.error(f"Gemini rate limit exceeded: {e}")
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again in a moment."
        )
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process query. Please try again."
        )
```

**Benefits**: User-friendly error messages, detailed logging for debugging, proper HTTP status codes.

---

### Pattern 4: React State Management for Chat

**Use React hooks for local state, avoid global state complexity**:
```jsx
function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);

  const sendMessage = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${apiUrl}/api/chat/query`, {
        query: input,
        history: messages.map(m => ({
          role: m.role,
          content: m.content
        })),
        selected_text: selectedText
      });

      setMessages([
        ...messages,
        { role: 'user', content: input },
        { role: 'assistant', content: response.data.response, sources: response.data.sources }
      ]);
      setInput('');
      setSelectedText(null);
    } catch (error) {
      // Show error message
    } finally {
      setIsLoading(false);
    }
  };

  return (
    // UI
  );
}
```

**Benefits**: Simple, predictable, no external dependencies (Redux, MobX), easy to test.

---

## Open Questions Resolved

1. **How to handle long conversations (>10 exchanges)?**
   - **Answer**: Implement sliding window (keep last 10 exchanges), summarize older context if needed
   - **Implementation**: In `rag_service.py`, slice history to last 10 before passing to Gemini

2. **Should we cache query results?**
   - **Answer**: Not for MVP (adds complexity, invalidation challenges)
   - **Future**: Consider Redis cache for common queries if performance becomes issue

3. **How to handle markdown in chat responses?**
   - **Answer**: Gemini returns plain text responses, citations are separate
   - **Frontend**: Render response as text, citations as links below

4. **Should we implement authentication?**
   - **Answer**: No (out of scope per spec constraint)
   - **Security**: Rate limit by IP, validate inputs, no PII in feedback

## Next Steps

1. ✅ Research complete
2. **Create data-model.md**: Define entities, schemas, relationships
3. **Create contracts/openapi.yaml**: API specification
4. **Create quickstart.md**: Setup and development guide
5. **Run `/sp.tasks`**: Generate implementation task breakdown
