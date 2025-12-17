# Implementation Plan: RAG Chatbot for Physical AI & Humanoid Robotics Book

**Branch**: `1-rag-chatbot` | **Date**: 2025-12-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-rag-chatbot/spec.md`

## Summary

Build an intelligent RAG (Retrieval-Augmented Generation) chatbot that integrates with the existing Physical AI & Humanoid Robotics Docusaurus book. The chatbot will enable readers to ask natural language questions about book content and receive accurate, citation-backed answers in under 3 seconds. The system uses Gemini API for embeddings and generation, Qdrant Cloud for vector search, and Neon Postgres for feedback storage. Implementation follows a clean separation between backend (FastAPI service in `rag-backend/`) and frontend (React components in Docusaurus `src/components/chat/`), ensuring the existing book structure remains untouched.

## Technical Context

**Language/Version**: Python 3.11+ (backend), Node.js 18+ with React 18 (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.109.0, google-generativeai 0.3.2, qdrant-client 1.7.0, psycopg2-binary 2.9.9, SQLAlchemy 2.0.25
- Frontend: axios 1.6.0, Docusaurus 3.x (existing)
**Storage**: Qdrant Cloud (768d vector embeddings), Neon Serverless Postgres (feedback, metadata)
**Testing**: pytest (backend), Jest/React Testing Library (frontend), Postman/curl (API contracts)
**Target Platform**: Linux/macOS development environment, deployed to Railway/Render (backend) + Vercel (frontend)
**Project Type**: Web application (separate backend API + frontend integration)
**Performance Goals**:
- <3s response time (95th percentile) for queries
- <10 minutes to index all book content (100+ markdown files)
- Support 50 concurrent users without degradation
**Constraints**:
- <5s for response generation (user engagement threshold)
- Gemini API rate limits (handled with exponential backoff)
- <200ms p95 for Qdrant vector search
- Maintain Docusaurus theme consistency
- Zero modifications to existing book content in `docs/`
**Scale/Scope**:
- ~100+ markdown files across 4 modules
- ~500-1000 chunks (each 500-1000 tokens)
- 10-exchange conversation history per session
- 2000 character query limit
- 1000 word selected text limit

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Alignment with Core Principles

✅ **Content Quality Standards**: Chatbot provides accurate, citation-backed answers directly from book content, maintaining technical accuracy.

✅ **Educational Structure**: Chatbot supports progressive learning by allowing students to query concepts at any point in their journey.

✅ **Technical Guidelines**:
- Python code follows PEP 8
- Environment configurations use `.env` files
- Secrets never committed (`.gitignore` includes `.env`)

✅ **RAG Chatbot Integration Standards**:
- Uses Gemini API for NLU and generation
- Backend implemented as separate FastAPI service
- Neon Serverless Postgres for metadata/feedback
- Qdrant Cloud Free Tier for vector embeddings
- All responses include citation links to source material

✅ **Project Structure and Integration**:
- Backend in `rag-backend/` (root level)
- Frontend in `physical-ai-humanoid-robotics/src/components/chat/`
- Existing book content structure untouched
- Chat widget accessible on all pages
- Independent deployability

✅ **Development Architecture**:
- Backend on `localhost:8000` during dev
- CORS configured for Docusaurus origin
- Secrets in `rag-backend/.env`
- Health check endpoint (`/api/health`)
- RESTful API with consistent JSON responses

✅ **User Experience and Accessibility**:
- Floating chat button on all pages
- Two query modes (full book + selected text)
- Clickable citation links
- Keyboard and screen-reader accessible
- Clear loading states and error messages
- Responsive design (mobile/tablet/desktop)

### Constitution Compliance Summary

**Status**: ✅ PASS - All constitution principles are satisfied.

**Key Alignments**:
1. Separate backend/frontend architecture per constitution
2. Gemini + Qdrant + Neon stack per RAG standards
3. Zero modifications to existing book structure
4. Citation-backed responses for academic integrity
5. Accessibility and UX requirements met

**No violations to justify.**

## Project Structure

### Documentation (this feature)

```text
specs/1-rag-chatbot/
├── spec.md              # Feature specification (✅ complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions, patterns)
├── data-model.md        # Phase 1 output (entities, schemas, database design)
├── quickstart.md        # Phase 1 output (setup, run, test instructions)
├── contracts/           # Phase 1 output (API specifications)
│   ├── openapi.yaml     # OpenAPI 3.0 spec for all endpoints
│   └── schemas.json     # Pydantic/JSON schemas
├── checklists/          # Quality validation
│   └── requirements.md  # Spec validation (✅ complete)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
robotic/
├── rag-backend/                          # NEW: Backend service
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                       # FastAPI app, CORS, middleware
│   │   ├── config.py                     # Pydantic Settings (env vars)
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                   # POST /api/chat/query, /feedback
│   │   │   └── admin.py                  # POST /api/index/refresh, GET /health
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── gemini_service.py         # Gemini API client (embeddings + generation)
│   │   │   ├── qdrant_service.py         # Qdrant vector operations
│   │   │   ├── neon_service.py           # Postgres queries (feedback, metadata)
│   │   │   └── rag_service.py            # Core RAG orchestration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py                # Pydantic request/response models
│   │   │   └── database.py               # SQLAlchemy ORM models
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── chunking.py               # Text splitting (500-1000 tokens)
│   │       ├── embedding.py              # Batch embedding generation
│   │       └── logger.py                 # Structured logging
│   ├── scripts/
│   │   └── index_book_content.py         # CLI tool to index docs/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                   # pytest fixtures
│   │   ├── test_routers/
│   │   │   ├── test_chat.py
│   │   │   └── test_admin.py
│   │   ├── test_services/
│   │   │   ├── test_rag_service.py
│   │   │   ├── test_gemini_service.py
│   │   │   └── test_qdrant_service.py
│   │   └── test_utils/
│   │       └── test_chunking.py
│   ├── requirements.txt                  # Python dependencies
│   ├── requirements-dev.txt              # Dev dependencies (pytest, black, etc.)
│   ├── .env.example                      # Template for environment variables
│   ├── .gitignore                        # Ignore .env, __pycache__, etc.
│   ├── pytest.ini                        # pytest configuration
│   └── README.md                         # Backend setup and API docs
│
├── physical-ai-humanoid-robotics/        # EXISTING: Docusaurus book
│   ├── src/
│   │   ├── components/
│   │   │   └── chat/                     # NEW: Chat components
│   │   │       ├── ChatWidget.jsx        # Main container (modal/sidebar)
│   │   │       ├── ChatButton.jsx        # Floating button (bottom-right)
│   │   │       ├── MessageList.jsx       # Message display with citations
│   │   │       ├── InputBox.jsx          # Input field + send button
│   │   │       ├── TextSelectionHandler.jsx  # Detect highlights
│   │   │       ├── FeedbackButtons.jsx   # Thumbs up/down
│   │   │       └── chat.css              # Component styles
│   │   ├── theme/
│   │   │   └── Root.js                   # NEW: Wrap app with ChatWidget
│   │   └── css/
│   │       └── custom.css                # EXISTING (no changes)
│   ├── docs/                             # EXISTING (no modifications)
│   │   ├── intro.md
│   │   ├── learning-outcomes.md
│   │   ├── module-1-ros2/
│   │   ├── module-2-digital-twin/
│   │   ├── module-3-nvidia-isaac/
│   │   └── module-4-vla/
│   ├── docusaurus.config.js              # UPDATE: Add customFields.ragApiUrl
│   ├── package.json                      # UPDATE: Add axios dependency
│   └── [other existing files]            # NO CHANGES
│
└── specs/
    └── 1-rag-chatbot/                    # Planning artifacts (this folder)
```

**Structure Decision**: Web application with separate backend API. Backend is a standalone FastAPI service in `rag-backend/` with complete isolation (own dependencies, tests, config). Frontend integration is minimal: new React components in `src/components/chat/`, theme wrapper in `src/theme/Root.js`, and config updates. This separation ensures:
1. Backend can be developed, tested, deployed independently
2. Docusaurus book remains functional even if backend is down
3. Clear ownership boundaries (Python devs for backend, React devs for frontend)
4. Easy to replace/upgrade either component without affecting the other

## Complexity Tracking

> **No violations - this section intentionally left empty.**

All architectural decisions align with the constitution. The separate backend/frontend structure is explicitly required by the RAG Chatbot Integration Standards and Development Architecture principles.

## Phase 0: Research & Technology Validation

### Research Questions

1. **Gemini API Integration Patterns**
   - What is the recommended way to handle Gemini rate limits and quotas?
   - How should we structure prompts for RAG with conversation history?
   - What are best practices for batch embedding generation?

2. **Qdrant Cloud Setup**
   - How to structure collections for optimal search performance?
   - What distance metric works best for text-embedding-004 (768d)?
   - How to handle collection updates during re-indexing?

3. **Markdown Parsing for Book Content**
   - How to extract frontmatter (module, section, title) from Docusaurus markdown?
   - What's the best approach for semantic chunking (respect headings, paragraphs)?
   - How to generate correct URL paths from file structure?

4. **Docusaurus Theme Integration**
   - How to properly swizzle components without breaking updates?
   - What's the correct way to access customFields in components?
   - How to ensure chat widget doesn't conflict with existing UI?

5. **Text Selection Detection in React**
   - What's the most reliable cross-browser method for detecting text selection?
   - How to position tooltip/action button near selection?
   - How to preserve selection state when opening chat?

### Research Outputs

See [research.md](./research.md) for detailed findings, technology decisions, and implementation patterns.

## Phase 1: Architecture & Contracts

### High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Reader)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Docusaurus Book                                        │ │
│  │  ┌──────────────┐  ┌──────────────────────────────┐   │ │
│  │  │ Book Pages   │  │  Chat Components              │   │ │
│  │  │ (docs/)      │  │  - ChatWidget.jsx             │   │ │
│  │  │              │  │  - ChatButton.jsx             │   │ │
│  │  │              │  │  - MessageList.jsx            │   │ │
│  │  │              │  │  - InputBox.jsx               │   │ │
│  │  │              │  │  - TextSelectionHandler.jsx   │   │ │
│  │  └──────────────┘  └──────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/JSON (axios)
                     │ POST /api/chat/query
                     │ POST /api/chat/feedback
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              rag-backend/ (FastAPI)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ API Routers                                            │ │
│  │  - chat.py: /query, /feedback                         │ │
│  │  - admin.py: /health, /index/refresh                  │ │
│  └──────────────┬─────────────────────────────────────────┘ │
│                 │                                            │
│  ┌──────────────▼─────────────────────────────────────────┐ │
│  │ RAG Service (Core Orchestration)                      │ │
│  │  1. Receive query + history + selected_text          │ │
│  │  2. Generate query embedding (Gemini)                │ │
│  │  3. Search Qdrant for top-N chunks                   │ │
│  │  4. Assemble context + prompt                        │ │
│  │  5. Generate response (Gemini)                       │ │
│  │  6. Extract citations from chunk metadata            │ │
│  └──────────┬────────────────────────┬──────────────────┘ │
│             │                        │                     │
│   ┌─────────▼────────┐    ┌──────────▼────────┐           │
│   │ Gemini Service   │    │ Qdrant Service    │           │
│   │ - embeddings     │    │ - vector search   │           │
│   │ - generation     │    │ - indexing        │           │
│   └──────────────────┘    └───────────────────┘           │
│                                                             │
│   ┌──────────────────────────────────────────────┐         │
│   │ Neon Service                                │         │
│   │ - store feedback                            │         │
│   │ - query metadata                            │         │
│   └──────────────────────────────────────────────┘         │
└─────────────────┬─────────────────┬─────────────────────────┘
                  │                 │
         ┌────────▼────────┐  ┌─────▼──────────┐
         │ Qdrant Cloud    │  │ Neon Postgres  │
         │ (Vectors)       │  │ (Feedback)     │
         └─────────────────┘  └────────────────┘
                  ▲
                  │ Indexing (one-time + refresh)
         ┌────────┴────────┐
         │ scripts/        │
         │ index_book_     │
         │ content.py      │
         └─────────────────┘
                  ▲
                  │ Reads markdown
         ┌────────┴────────┐
         │ physical-ai-    │
         │ humanoid-       │
         │ robotics/docs/  │
         └─────────────────┘
```

### Data Flow: Query Processing

1. **User initiates query**:
   - User types question in ChatWidget InputBox OR
   - User highlights text, clicks "Ask about this text", types follow-up

2. **Frontend sends request**:
   ```json
   POST /api/chat/query
   {
     "query": "How do ROS 2 nodes communicate?",
     "history": [
       {"role": "user", "content": "What is ROS 2?"},
       {"role": "assistant", "content": "ROS 2 is...", "sources": [...]}
     ],
     "selected_text": null  // or highlighted text
   }
   ```

3. **Backend RAG pipeline**:
   - `chat.py` router validates request (Pydantic schema)
   - `rag_service.py` orchestrates:
     - Generate query embedding via `gemini_service.py`
     - Search Qdrant for top-7 similar chunks via `qdrant_service.py`
     - Build prompt with retrieved context + history
     - Generate response via `gemini_service.py`
     - Extract citations from chunk metadata

4. **Backend returns response**:
   ```json
   {
     "response": "ROS 2 nodes communicate using DDS...",
     "sources": [
       {
         "module": "module-1-ros2",
         "section": "week-3-fundamentals",
         "url": "/module-1-ros2/week-3-fundamentals"
       }
     ]
   }
   ```

5. **Frontend displays**:
   - MessageList shows AI response
   - Citations rendered as clickable links
   - FeedbackButtons appear below message

### Data Model

See [data-model.md](./data-model.md) for detailed entity definitions, relationships, and database schemas.

### API Contracts

See [contracts/openapi.yaml](./contracts/openapi.yaml) for complete OpenAPI 3.0 specification.

**Endpoint Summary**:
- `POST /api/chat/query` - Submit query and receive RAG response
- `POST /api/chat/feedback` - Submit feedback on a response
- `GET /api/health` - Health check (returns DB/API status)
- `POST /api/index/refresh` - Trigger book content re-indexing (admin)

### Quickstart Guide

See [quickstart.md](./quickstart.md) for step-by-step setup, development, and testing instructions.

## Phase 2: Implementation Tasks

**Not included in this document.** Use `/sp.tasks` command to generate detailed, prioritized task breakdown based on this plan.

## Implementation Phases (Overview)

### Phase 1: Backend Foundation (P1 - Core Infrastructure)
- Setup FastAPI project structure
- Implement configuration management (`config.py`, `.env`)
- Setup Gemini API client (`gemini_service.py`)
- Setup Qdrant connection (`qdrant_service.py`)
- Setup Neon Postgres connection (`neon_service.py`)
- Create Pydantic schemas (`schemas.py`)
- Implement health check endpoint
- Write unit tests for services

### Phase 2: Data Indexing (P1 - Required for Query)
- Implement markdown parsing (frontmatter, content)
- Implement semantic chunking (`chunking.py`)
- Implement batch embedding generation (`embedding.py`)
- Create Qdrant collection schema
- Implement indexing script (`index_book_content.py`)
- Create Neon database schema (feedback table)
- Test indexing with sample module
- Index all book modules

### Phase 3: RAG Service (P1 - Core Functionality)
- Implement query embedding generation
- Implement Qdrant vector search
- Implement context assembly (retrieved chunks + history)
- Implement prompt engineering for Gemini
- Implement response generation
- Implement citation extraction
- Handle conversation history (sliding window)
- Write integration tests

### Phase 4: API Endpoints (P1 - External Interface)
- Implement `/api/chat/query` endpoint
- Implement `/api/chat/feedback` endpoint
- Implement `/api/index/refresh` endpoint
- Setup CORS middleware
- Implement error handling and validation
- Add request/response logging
- Test all endpoints with Postman
- Document API usage

### Phase 5: Frontend Components (P1 - User Interface)
- Create ChatButton component (floating button)
- Create ChatWidget component (modal/sidebar)
- Create MessageList component (display messages + citations)
- Create InputBox component (input + send)
- Implement chat.css (styling)
- Connect to backend API (axios)
- Handle loading states and errors
- Test with mock data

### Phase 6: Text Selection (P2 - Enhanced UX)
- Implement TextSelectionHandler component
- Detect text selection events
- Show "Ask about this text" tooltip
- Pass selected text to ChatWidget
- Integrate with query endpoint
- Test across browsers

### Phase 7: Conversation Memory (P3 - Multi-turn)
- Implement history state management
- Pass history in API requests
- Implement sliding window (10 exchanges)
- Persist history in session storage
- Clear history on new session
- Test multi-turn conversations

### Phase 8: Feedback Mechanism (P4 - Quality)
- Create FeedbackButtons component (thumbs up/down)
- Implement feedback submission UI
- Connect to `/api/chat/feedback` endpoint
- Store feedback in Neon Postgres
- Test feedback logging

### Phase 9: Docusaurus Integration (P1 - Deployment)
- Create `src/theme/Root.js` wrapper
- Update `docusaurus.config.js` (customFields)
- Update `package.json` (add axios)
- Test chat widget on all pages
- Verify no conflicts with existing UI
- Test responsive design

### Phase 10: Testing & Documentation (P1 - Quality Assurance)
- Write backend unit tests (pytest)
- Write frontend component tests (Jest)
- Write integration tests (full flow)
- Test with sample queries from each module
- Write backend README (setup, API docs)
- Create `.env.example` with all variables
- Document deployment instructions
- Create troubleshooting guide

## Risk Analysis & Mitigation

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Gemini API rate limits exceeded | HIGH | MEDIUM | Implement exponential backoff, queue requests, monitor quota usage, add user-facing rate limit messages |
| Qdrant Cloud free tier storage limit | MEDIUM | LOW | Monitor collection size, implement chunking limits, have migration plan to paid tier if needed |
| Neon Postgres connection limits | MEDIUM | LOW | Use connection pooling (SQLAlchemy), implement retry logic, monitor concurrent connections |
| Slow response times (>3s) | HIGH | MEDIUM | Optimize Qdrant search (limit top-N), cache common queries, use streaming responses for long generation |
| Docusaurus theme conflicts | MEDIUM | LOW | Use CSS modules for chat components, test across Docusaurus versions, avoid global CSS overrides |
| Text selection detection failures | LOW | MEDIUM | Test across browsers (Chrome, Firefox, Safari, Edge), provide fallback to manual copy-paste |

### Operational Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| API keys exposed in code | CRITICAL | LOW | Use `.env` files, add `.env` to `.gitignore`, audit commits, use secret scanning tools |
| Backend downtime during indexing | MEDIUM | LOW | Run indexing in background job, maintain service availability, add progress indicators |
| Book content updates require re-indexing | LOW | HIGH | Provide `/api/index/refresh` endpoint, document refresh process, automate with webhooks if possible |
| Frontend bundle size increase | LOW | MEDIUM | Code-split chat components, lazy load when chat opens, monitor bundle size in CI |

### User Experience Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Inaccurate or hallucinated responses | HIGH | MEDIUM | Ground responses in retrieved chunks only, add citations for verification, implement feedback mechanism, tune prompt engineering |
| Poor citation quality (irrelevant links) | MEDIUM | MEDIUM | Improve chunking strategy, tune Qdrant search parameters, filter low-confidence results |
| Chat widget obstructs content | MEDIUM | LOW | Position button in bottom-right, make draggable, add minimize/close options, test on small screens |
| Slow initial load (large chat component) | LOW | MEDIUM | Lazy load chat on first open, optimize React component rendering, use code splitting |

## Success Metrics & Validation

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| Query response time (p95) | <3 seconds | Load testing with k6/Locust, monitor in production with logging |
| Indexing time (all modules) | <10 minutes | Time script execution, optimize chunk generation and API calls |
| Citation accuracy | >80% relevant | Manual review of 100 sample queries, user feedback analysis |
| System uptime | >95% | Health check monitoring, uptime tracking (UptimeRobot) |
| Concurrent user support | 50 users | Load testing with gradual ramp-up, monitor response times under load |
| Conversation context preservation | 10 exchanges | Integration tests with multi-turn conversations, verify context in responses |
| Cross-browser compatibility | 100% (Chrome, Firefox, Safari, Edge) | Manual testing on each browser, automated E2E tests with Playwright |
| Accessibility | WCAG 2.1 AA | Automated testing (axe-core), keyboard navigation testing, screen reader testing |

## Next Steps

1. **Run `/sp.tasks`** to generate detailed, prioritized task breakdown
2. **Start with Phase 0 research** (immediate): Validate Gemini integration patterns, Qdrant setup, markdown parsing
3. **Backend development first** (Phase 1-4): Get RAG pipeline working before frontend integration
4. **Iterative frontend development** (Phase 5-9): Build components incrementally, test with backend
5. **Final integration and testing** (Phase 10): End-to-end validation, deployment prep

## Appendix: Technology Choices

### Why Gemini API?
- **Unified platform**: Single API for both embeddings (text-embedding-004, 768d) and generation (gemini-1.5-flash)
- **Cost-effective**: Generous free tier for development, competitive pricing for production
- **Performance**: Low latency, high quality embeddings and generation
- **Simplicity**: Easy integration via `google-generativeai` Python library

### Why Qdrant Cloud?
- **Free tier**: 1GB storage sufficient for book content (~500-1000 chunks)
- **Performance**: <200ms search latency for 768d vectors
- **Ease of use**: Simple API, Python client, managed service (no ops overhead)
- **Scalability**: Can upgrade to paid tier if needed

### Why Neon Postgres?
- **Serverless**: Auto-scaling, pay-per-use, no idle costs
- **Free tier**: Sufficient for feedback storage (low write volume)
- **Postgres compatibility**: Standard SQL, SQLAlchemy ORM support
- **Managed service**: No database administration required

### Why FastAPI?
- **Performance**: Async support, fast request handling
- **Developer experience**: Auto-generated OpenAPI docs, Pydantic validation
- **Python ecosystem**: Easy integration with Gemini, Qdrant, Neon libraries
- **Production-ready**: CORS, middleware, error handling built-in

### Why Docusaurus Integration (vs. Standalone Chat App)?
- **User experience**: Chat available while reading, no context switching
- **SEO**: Keep book content indexed, chat enhances existing pages
- **Simplicity**: Single deployment, single URL, unified branding
- **Constitution compliance**: Explicitly required by RAG Chatbot Integration Standards
