# Data Model: RAG Chatbot

**Feature**: 1-rag-chatbot
**Date**: 2025-12-15
**Purpose**: Define entities, relationships, schemas, and database design

## Entity Definitions

### 1. Chunk (Vector Database - Qdrant)

Represents a piece of indexed book content with its embedding.

**Attributes**:
- `id` (UUID, primary key): Unique identifier for the chunk (auto-generated)
- `chunk_id` (string): Human-readable identifier (e.g., "m1_w3_c1")
- `module` (string): Module name (e.g., "module-1-ros2")
- `section` (string): Section/chapter name (e.g., "week-3-fundamentals")
- `title` (string): Section title (e.g., "ROS 2 Architecture")
- `url` (string): Relative URL path (e.g., "/module-1-ros2/week-3-fundamentals")
- `content` (string): Actual text content (500-1000 tokens)
- `token_count` (integer): Number of tokens in content
- `embedding` (vector[768]): 768-dimensional embedding from Gemini

**Validation Rules**:
- `chunk_id` must match pattern: `m\d+_\w+_c\d+` (e.g., m1_w3_c1)
- `content` must be 500-1000 tokens (enforced during chunking)
- `token_count` must match actual content length
- `url` must start with `/`
- `embedding` must be 768 dimensions (validated by Qdrant)

**Storage**: Qdrant Cloud collection `book_chunks`

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "chunk_id": "m1_w3_c1",
  "module": "module-1-ros2",
  "section": "week-3-fundamentals",
  "title": "ROS 2 Architecture",
  "url": "/module-1-ros2/week-3-fundamentals",
  "content": "ROS 2 uses a Data Distribution Service (DDS) middleware...",
  "token_count": 756,
  "embedding": [0.023, -0.145, 0.089, ...]  // 768 dimensions
}
```

---

### 2. Source (API Response - Ephemeral)

Represents a citation linking a response to book content.

**Attributes**:
- `module` (string): Module name (e.g., "module-1-ros2")
- `section` (string): Section name (e.g., "week-3-fundamentals")
- `url` (string): Clickable link to content (e.g., "/module-1-ros2/week-3-fundamentals")
- `relevance_score` (float, optional): Similarity score from Qdrant search (0.0-1.0)

**Validation Rules**:
- `module` must match pattern: `module-\d+-[\w-]+`
- `url` must be a valid relative path starting with `/`
- `relevance_score` (if provided) must be 0.0-1.0

**Storage**: Not persisted; returned in API responses only

**Example**:
```json
{
  "module": "module-1-ros2",
  "section": "week-3-fundamentals",
  "url": "/module-1-ros2/week-3-fundamentals",
  "relevance_score": 0.87
}
```

---

### 3. ChatMessage (API Request/Response - Ephemeral)

Represents a single message in a conversation.

**Attributes**:
- `role` (enum: "user" | "assistant"): Message sender
- `content` (string): Message text
- `sources` (array[Source], optional): Citations (only for assistant messages)
- `timestamp` (datetime, optional): When message was sent

**Validation Rules**:
- `role` must be "user" or "assistant"
- `content` must be non-empty, max 2000 characters for user messages
- `sources` only valid when `role` is "assistant"

**Storage**: Not persisted; exists only in conversation history (in-memory, session storage on frontend)

**Example**:
```json
{
  "role": "user",
  "content": "How do ROS 2 nodes communicate?",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

```json
{
  "role": "assistant",
  "content": "ROS 2 nodes communicate using DDS (Data Distribution Service)...",
  "sources": [
    {
      "module": "module-1-ros2",
      "section": "week-3-fundamentals",
      "url": "/module-1-ros2/week-3-fundamentals"
    }
  ],
  "timestamp": "2025-12-15T10:30:02Z"
}
```

---

### 4. Feedback (Relational Database - Neon Postgres)

Represents user feedback on a chatbot response.

**Attributes**:
- `id` (UUID, primary key): Unique identifier
- `query` (text): Original user question
- `response` (text): Chatbot's answer
- `selected_text` (text, nullable): Highlighted text context (if Mode B query)
- `rating` (integer): 1 (thumbs up) or -1 (thumbs down)
- `comment` (text, nullable): Optional written feedback from user
- `timestamp` (timestamp): When feedback was submitted
- `session_id` (string, nullable): Browser session identifier (for grouping)
- `sources_json` (jsonb, nullable): Citations that were shown (stored as JSON array)

**Validation Rules**:
- `query` must be non-empty, max 2000 characters
- `response` must be non-empty
- `rating` must be 1 or -1
- `comment` max 1000 characters
- `timestamp` defaults to current time
- `sources_json` must be valid JSON array of Source objects

**Indexes**:
- Primary key on `id`
- Index on `timestamp` (for date range queries)
- Index on `rating` (for filtering positive/negative feedback)

**Storage**: Neon Postgres table `feedback`

**SQL Schema**:
```sql
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    selected_text TEXT,
    rating INTEGER NOT NULL CHECK (rating IN (1, -1)),
    comment TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    session_id VARCHAR(255),
    sources_json JSONB,
    CONSTRAINT query_length CHECK (LENGTH(query) <= 2000),
    CONSTRAINT comment_length CHECK (comment IS NULL OR LENGTH(comment) <= 1000)
);

CREATE INDEX idx_feedback_timestamp ON feedback(timestamp);
CREATE INDEX idx_feedback_rating ON feedback(rating);
```

**Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "query": "How do ROS 2 nodes communicate?",
  "response": "ROS 2 nodes communicate using DDS...",
  "selected_text": null,
  "rating": 1,
  "comment": "Very helpful explanation!",
  "timestamp": "2025-12-15T10:35:00Z",
  "session_id": "abc123def456",
  "sources_json": [
    {
      "module": "module-1-ros2",
      "section": "week-3-fundamentals",
      "url": "/module-1-ros2/week-3-fundamentals"
    }
  ]
}
```

---

### 5. QueryRequest (API Request - Pydantic Schema)

Request payload for `/api/chat/query` endpoint.

**Attributes**:
- `query` (string): User's question
- `history` (array[ChatMessage]): Previous conversation messages
- `selected_text` (string, optional): Highlighted text from book (Mode B)

**Validation Rules**:
- `query` must be non-empty, max 2000 characters
- `history` max 10 messages (sliding window)
- `selected_text` (if provided) max 5000 characters (~1000 words)

**Pydantic Schema**:
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=10000)
    sources: Optional[List[Source]] = None

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    history: List[ChatMessage] = Field(default_factory=list, max_items=10)
    selected_text: Optional[str] = Field(None, max_length=5000)

    @validator('query')
    def query_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()
```

**Example**:
```json
{
  "query": "How do I set it up?",
  "history": [
    {
      "role": "user",
      "content": "What is NVIDIA Isaac?"
    },
    {
      "role": "assistant",
      "content": "NVIDIA Isaac is a platform for robotics simulation...",
      "sources": [
        {
          "module": "module-3-nvidia-isaac",
          "section": "week-8-intro",
          "url": "/module-3-nvidia-isaac/week-8-intro"
        }
      ]
    }
  ],
  "selected_text": null
}
```

---

### 6. QueryResponse (API Response - Pydantic Schema)

Response payload for `/api/chat/query` endpoint.

**Attributes**:
- `response` (string): Generated answer from chatbot
- `sources` (array[Source]): Citations with links to book content

**Validation Rules**:
- `response` must be non-empty
- `sources` must contain at least 1 source (unless query is out-of-scope)

**Pydantic Schema**:
```python
from pydantic import BaseModel, Field
from typing import List

class Source(BaseModel):
    module: str = Field(..., pattern="^module-\\d+-[\\w-]+$")
    section: str
    url: str = Field(..., pattern="^/.*")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class QueryResponse(BaseModel):
    response: str = Field(..., min_length=1)
    sources: List[Source] = Field(default_factory=list)
```

**Example**:
```json
{
  "response": "To set up NVIDIA Isaac Sim, you need to first install Omniverse Launcher...",
  "sources": [
    {
      "module": "module-3-nvidia-isaac",
      "section": "week-8-setup",
      "url": "/module-3-nvidia-isaac/week-8-setup",
      "relevance_score": 0.92
    },
    {
      "module": "module-3-nvidia-isaac",
      "section": "week-8-intro",
      "url": "/module-3-nvidia-isaac/week-8-intro",
      "relevance_score": 0.78
    }
  ]
}
```

---

### 7. FeedbackRequest (API Request - Pydantic Schema)

Request payload for `/api/chat/feedback` endpoint.

**Attributes**:
- `query` (string): Original user question
- `response` (string): Chatbot's answer
- `selected_text` (string, optional): Context from Mode B query
- `rating` (integer): 1 (thumbs up) or -1 (thumbs down)
- `comment` (string, optional): Written feedback
- `session_id` (string, optional): Browser session ID
- `sources` (array[Source], optional): Citations that were shown

**Pydantic Schema**:
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class FeedbackRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    response: str = Field(..., min_length=1)
    selected_text: Optional[str] = Field(None, max_length=5000)
    rating: int = Field(..., ge=-1, le=1)
    comment: Optional[str] = Field(None, max_length=1000)
    session_id: Optional[str] = None
    sources: Optional[List[Source]] = None

    @validator('rating')
    def rating_valid(cls, v):
        if v not in [1, -1]:
            raise ValueError('Rating must be 1 (thumbs up) or -1 (thumbs down)')
        return v
```

**Example**:
```json
{
  "query": "How do ROS 2 nodes communicate?",
  "response": "ROS 2 nodes communicate using DDS...",
  "selected_text": null,
  "rating": -1,
  "comment": "Answer was too technical for beginners",
  "session_id": "abc123def456",
  "sources": [
    {
      "module": "module-1-ros2",
      "section": "week-3-fundamentals",
      "url": "/module-1-ros2/week-3-fundamentals"
    }
  ]
}
```

---

### 8. IndexingJob (Backend State - Optional, Future Enhancement)

Represents a content indexing operation. *Not implemented in MVP; included for future reference.*

**Attributes**:
- `job_id` (UUID): Unique identifier
- `status` (enum: "running" | "completed" | "failed"): Job status
- `start_time` (timestamp): When indexing started
- `end_time` (timestamp, nullable): When indexing finished
- `chunks_processed` (integer): Number of chunks indexed
- `errors` (array[string]): Error messages encountered

**Storage**: Could be stored in Neon Postgres or in-memory (Redis) for MVP

---

## Entity Relationships

```text
┌─────────────────────────┐
│ Chunk (Qdrant)          │
│ - id (PK)               │
│ - chunk_id              │
│ - module                │
│ - section               │
│ - title                 │
│ - url                   │
│ - content               │
│ - token_count           │
│ - embedding [768]       │
└────────────┬────────────┘
             │
             │ Referenced by (via module, section, url)
             │
             ▼
┌─────────────────────────┐
│ Source (Ephemeral)      │
│ - module                │
│ - section               │
│ - url                   │
│ - relevance_score       │
└────────────┬────────────┘
             │
             │ Part of
             │
             ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│ QueryResponse           │       │ ChatMessage             │
│ - response              │       │ - role                  │
│ - sources []            │       │ - content               │
└─────────────────────────┘       │ - sources []            │
                                  │ - timestamp             │
                                  └────────────┬────────────┘
                                               │
                                               │ Part of history
                                               │
                                               ▼
                                  ┌─────────────────────────┐
                                  │ QueryRequest            │
                                  │ - query                 │
                                  │ - history []            │
                                  │ - selected_text         │
                                  └─────────────────────────┘

┌─────────────────────────┐
│ Feedback (Postgres)     │
│ - id (PK)               │
│ - query                 │
│ - response              │
│ - selected_text         │
│ - rating                │
│ - comment               │
│ - timestamp             │
│ - session_id            │
│ - sources_json          │
└─────────────────────────┘
(Independent entity, no foreign keys)
```

**Relationship Notes**:
- **Chunk ↔ Source**: Loose coupling via matching `module`, `section`, `url` fields. Source is derived from Chunk metadata during RAG pipeline.
- **QueryRequest ↔ QueryResponse**: Request-response pair in API. No persistent relationship.
- **ChatMessage**: Used in both request history and response format. Ephemeral, stored client-side in session.
- **Feedback**: Independent entity, stores snapshot of query/response/sources for analysis. No foreign keys to other entities.

---

## Database Schemas

### Qdrant Collection: `book_chunks`

**Configuration**:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="book_chunks",
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE
    ),
    optimizers_config={
        "indexing_threshold": 10000,
        "memmap_threshold": 20000
    },
    hnsw_config={
        "m": 16,
        "ef_construct": 100
    }
)
```

**Point Structure**:
```json
{
  "id": "uuid-string",
  "vector": [0.023, -0.145, ...],  // 768 floats
  "payload": {
    "chunk_id": "m1_w3_c1",
    "module": "module-1-ros2",
    "section": "week-3-fundamentals",
    "title": "ROS 2 Architecture",
    "url": "/module-1-ros2/week-3-fundamentals",
    "content": "ROS 2 uses DDS...",
    "token_count": 756
  }
}
```

**Indexes**: HNSW (Hierarchical Navigable Small World) automatically built by Qdrant for fast approximate nearest neighbor search.

---

### Neon Postgres: `feedback` Table

**Schema** (see Feedback entity above for SQL):
```sql
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    selected_text TEXT,
    rating INTEGER NOT NULL CHECK (rating IN (1, -1)),
    comment TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    session_id VARCHAR(255),
    sources_json JSONB,
    CONSTRAINT query_length CHECK (LENGTH(query) <= 2000),
    CONSTRAINT comment_length CHECK (comment IS NULL OR LENGTH(comment) <= 1000)
);

CREATE INDEX idx_feedback_timestamp ON feedback(timestamp);
CREATE INDEX idx_feedback_rating ON feedback(rating);
```

**SQLAlchemy ORM Model**:
```python
from sqlalchemy import Column, String, Text, Integer, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Feedback(Base):
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
        CheckConstraint('comment IS NULL OR LENGTH(comment) <= 1000', name='comment_length_check'),
    )
```

---

## Data Validation Rules Summary

| Entity | Field | Rule |
|--------|-------|------|
| Chunk | chunk_id | Pattern: `m\d+_\w+_c\d+` |
| Chunk | content | 500-1000 tokens |
| Chunk | token_count | Must match content length |
| Chunk | url | Must start with `/` |
| Chunk | embedding | Must be 768 dimensions |
| Source | module | Pattern: `module-\d+-[\w-]+` |
| Source | url | Must start with `/` |
| Source | relevance_score | 0.0-1.0 (if provided) |
| ChatMessage | role | "user" or "assistant" |
| ChatMessage | content | Non-empty, max 2000 chars (user), 10000 chars (assistant) |
| QueryRequest | query | Non-empty, max 2000 chars |
| QueryRequest | history | Max 10 messages |
| QueryRequest | selected_text | Max 5000 chars (if provided) |
| QueryResponse | response | Non-empty |
| Feedback | query | Non-empty, max 2000 chars |
| Feedback | rating | 1 or -1 |
| Feedback | comment | Max 1000 chars (if provided) |

---

## Migration Strategy

### Initial Setup

1. **Qdrant Collection**:
   - Create `book_chunks` collection with config above
   - Run indexing script to populate

2. **Neon Postgres**:
   - Create `feedback` table with SQL schema
   - Apply indexes

### Schema Updates (Future)

**Qdrant**:
- Collection schema is fixed after creation
- To update: Create new collection, re-index, swap (or use versioned collections: `book_chunks_v1`, `book_chunks_v2`)

**Postgres**:
- Use Alembic for migrations
- Example: Add new column to `feedback` table
  ```sql
  ALTER TABLE feedback ADD COLUMN user_agent TEXT;
  ```

---

## Performance Considerations

### Qdrant

- **Search Latency**: <200ms for 768d vector search with HNSW index
- **Indexing**: ~1-2 seconds per 100 chunks (embedding generation dominates)
- **Storage**: ~1KB per chunk payload + ~3KB per vector = ~4KB per chunk total
  - 1000 chunks = ~4MB (well within 1GB free tier)

### Neon Postgres

- **Write Latency**: <50ms for feedback inserts (low volume)
- **Storage**: ~500 bytes per feedback row (text fields compressed)
  - 10,000 feedback entries = ~5MB
- **Query Performance**: Timestamp/rating indexes ensure fast filtering (<10ms)

### API Response Times

- **Query Processing**:
  - Embedding generation: ~500ms (Gemini API)
  - Qdrant search: ~100ms
  - Response generation: ~1-2s (Gemini API, depends on length)
  - **Total**: ~2-3s (within <3s target)

- **Feedback Submission**: <100ms (simple INSERT)

---

## Security & Privacy

### Data Protection

- **API Keys**: Never stored in database; only in environment variables
- **User Queries**: Stored in feedback only if user submits feedback
- **Session IDs**: Optional, used only for grouping feedback; not linked to PII
- **No PII Collection**: System doesn't collect names, emails, or identifiable information

### Input Sanitization

- **SQL Injection**: Prevented by SQLAlchemy parameterized queries
- **XSS**: Frontend sanitizes user input before rendering
- **Prompt Injection**: Query validation (max length, character filtering) limits attack surface
- **Rate Limiting**: Implement per-IP rate limits in API (e.g., 100 requests/hour)

---

## Testing Data

### Sample Chunks (for Testing)

```python
sample_chunks = [
    {
        "chunk_id": "m1_w1_c1",
        "module": "module-1-ros2",
        "section": "week-1-intro",
        "title": "Introduction to ROS 2",
        "url": "/module-1-ros2/week-1-intro",
        "content": "ROS 2 (Robot Operating System 2) is the next-generation robot middleware...",
        "token_count": 512
    },
    {
        "chunk_id": "m3_w8_c1",
        "module": "module-3-nvidia-isaac",
        "section": "week-8-intro",
        "title": "NVIDIA Isaac Overview",
        "url": "/module-3-nvidia-isaac/week-8-intro",
        "content": "NVIDIA Isaac is a platform for developing, testing, and deploying AI-powered robots...",
        "token_count": 789
    }
]
```

### Sample Queries (for Testing)

```python
test_queries = [
    "What is ROS 2?",
    "How do I install NVIDIA Isaac Sim?",
    "Explain DDS communication in ROS 2",
    "What are the benefits of using Gazebo for simulation?",
    "How does VLA work with physical robots?"
]
```

---

## Next Steps

1. ✅ Data model defined
2. **Create API contracts** (OpenAPI spec in `contracts/openapi.yaml`)
3. **Implement Pydantic schemas** in `app/models/schemas.py`
4. **Implement SQLAlchemy models** in `app/models/database.py`
5. **Create database initialization script** (create tables, indexes)
6. **Write unit tests for data validation**
