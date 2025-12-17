# Tasks: RAG Chatbot for Physical AI & Humanoid Robotics Book

**Input**: Design documents from `/specs/1-rag-chatbot/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are NOT requested in the specification. Test tasks are excluded from this plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- All tasks include exact file paths

## Path Conventions

- **Backend**: `rag-backend/app/`, `rag-backend/scripts/`, `rag-backend/tests/`
- **Frontend**: `physical-ai-humanoid-robotics/src/components/chat/`, `physical-ai-humanoid-robotics/src/theme/`
- Paths are absolute from repository root (`/mnt/d/robotic/`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

- [x] T001 Create backend directory structure (rag-backend/app/, routers/, services/, models/, utils/, scripts/, tests/)
- [x] T002 [P] Create backend __init__.py files in rag-backend/app/, app/routers/, app/services/, app/models/, app/utils/
- [x] T003 [P] Create frontend chat directory structure (physical-ai-humanoid-robotics/src/components/chat/)
- [x] T004 Create rag-backend/requirements.txt with dependencies (FastAPI, google-generativeai, qdrant-client, psycopg2-binary, SQLAlchemy, pydantic, etc.)
- [x] T005 [P] Create rag-backend/requirements-dev.txt with dev dependencies (pytest, black, flake8, mypy)
- [x] T006 [P] Create rag-backend/.env.example with environment variable templates
- [x] T007 [P] Create rag-backend/.gitignore (ignore .env, __pycache__, venv/, .pytest_cache/)
- [x] T008 [P] Create rag-backend/pytest.ini with pytest configuration
- [X] T009 Initialize Python virtual environment and install dependencies (as per quickstart.md)
- [x] T010 [P] Add axios dependency to physical-ai-humanoid-robotics/package.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Create rag-backend/app/config.py with Pydantic Settings for environment variables (GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DATABASE_URL, BOOK_CONTENT_PATH, ALLOWED_ORIGINS)
- [x] T012 Create rag-backend/app/main.py with FastAPI app, CORS middleware, root endpoint
- [x] T013 [P] Create rag-backend/app/models/schemas.py with Pydantic models (Source, ChatMessage, QueryRequest, QueryResponse, FeedbackRequest)
- [x] T014 [P] Create rag-backend/app/models/database.py with SQLAlchemy Feedback model
- [x] T015 Create rag-backend/scripts/setup_database.py to create Neon Postgres feedback table with indexes
- [x] T016 Create rag-backend/scripts/setup_qdrant.py to create Qdrant collection (book_chunks, 768d, COSINE distance)
- [X] T017 Run setup_database.py to initialize Neon Postgres schema
- [X] T018 Run setup_qdrant.py to create Qdrant collection
- [x] T019 Create rag-backend/app/utils/logger.py with structured logging configuration
- [x] T020 [P] Create rag-backend/app/routers/admin.py with health check endpoint (GET /api/health)
- [x] T021 Update rag-backend/app/main.py to include admin router
- [X] T022 Test health check endpoint returns status, timestamp, services, version

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Full Book Search and Query (Priority: P1) 🎯 MVP

**Goal**: Enable readers to ask natural language questions about book content and receive accurate, citation-backed answers with <3s response time. This is the core RAG functionality.

**Independent Test**: Ask questions about content from different modules (e.g., "What is ROS 2?", "How does NVIDIA Isaac work?") and verify responses include accurate information with proper source citations linking back to book sections.

### Backend: Content Indexing (US1 Foundation)

- [ ] T023 [P] [US1] Create rag-backend/app/utils/chunking.py with semantic chunking function (500-1000 tokens, heading-based, using tiktoken)
- [ ] T024 [P] [US1] Create rag-backend/app/utils/embedding.py with batch embedding generation (Gemini text-embedding-004, batch size 50, exponential backoff)
- [ ] T025 [US1] Create rag-backend/scripts/index_book_content.py to read markdown files from ../physical-ai-humanoid-robotics/docs/, parse frontmatter, chunk content, generate embeddings, upload to Qdrant
- [ ] T026 [US1] Run indexing script to populate Qdrant with book content (~500-1000 chunks from all 4 modules)
- [ ] T027 [US1] Verify Qdrant collection contains all chunks with correct metadata (chunk_id, module, section, title, url, content, token_count)

### Backend: RAG Service (US1 Core Logic)

- [ ] T028 [P] [US1] Create rag-backend/app/services/gemini_service.py with methods for generate_embedding() and generate_response() using google-generativeai SDK with exponential backoff
- [ ] T029 [P] [US1] Create rag-backend/app/services/qdrant_service.py with search() method to query Qdrant collection (top-7 chunks, COSINE distance, 0.7 score threshold)
- [ ] T030 [US1] Create rag-backend/app/services/rag_service.py with process_query() method orchestrating: (1) generate query embedding, (2) search Qdrant, (3) assemble context from chunks, (4) generate response with Gemini, (5) extract citations from chunk metadata
- [ ] T031 [US1] Implement prompt engineering in rag_service.py (context-first format, system instructions, citation requirements, out-of-scope handling)
- [ ] T032 [US1] Implement citation extraction in rag_service.py (convert chunk metadata to Source objects with module, section, url)

### Backend: Query API Endpoint (US1 External Interface)

- [ ] T033 [US1] Create rag-backend/app/routers/chat.py with POST /api/chat/query endpoint accepting QueryRequest (query, history, selected_text)
- [ ] T034 [US1] Implement /api/chat/query endpoint calling rag_service.process_query() and returning QueryResponse (response, sources)
- [ ] T035 [US1] Add error handling in /api/chat/query for rate limits (429), validation errors (400), internal errors (500)
- [ ] T036 [US1] Add request/response logging in chat router with query text, response length, sources count, processing time
- [ ] T037 [US1] Update rag-backend/app/main.py to include chat router with prefix /api/chat
- [ ] T038 [US1] Test /api/chat/query endpoint with Postman/curl (sample query: "What is ROS 2?") and verify response includes accurate answer with citations

### Frontend: Chat Button (US1 UI Foundation)

- [X] T039 [P] [US1] Create physical-ai-humanoid-robotics/src/components/chat/ChatButton.jsx with floating button component (bottom-right, emoji icon, onClick handler)
- [X] T040 [P] [US1] Create physical-ai-humanoid-robotics/src/components/chat/chat.css with styles for chat button (fixed position, z-index 1000, hover effect, responsive)

### Frontend: Chat Widget Container (US1 UI Core)

- [X] T041 [US1] Create physical-ai-humanoid-robotics/src/components/chat/ChatWidget.jsx with state management (isOpen, messages, input, isLoading)
- [X] T042 [US1] Implement ChatWidget UI structure (header with title and close button, body for messages, footer for input)
- [X] T043 [US1] Add chat container styles to chat.css (fixed position, width 400px, height 500px, modal/sidebar, Docusaurus theme variables)
- [X] T044 [US1] Integrate ChatButton into ChatWidget (toggle isOpen state on click)

### Frontend: Message List (US1 UI Display)

- [X] T045 [P] [US1] Create physical-ai-humanoid-robotics/src/components/chat/MessageList.jsx to display messages (user/assistant roles, content, sources)
- [X] T046 [US1] Implement citation rendering in MessageList (Source objects as clickable links with module, section, url)
- [X] T047 [US1] Add message list styles to chat.css (scrollable, user/assistant message differentiation, citation link styling)

### Frontend: Input Box (US1 UI Input)

- [X] T048 [P] [US1] Create physical-ai-humanoid-robotics/src/components/chat/InputBox.jsx with input field, send button, character counter (max 2000)
- [X] T049 [US1] Implement input validation in InputBox (non-empty, max 2000 characters, disable during loading)
- [X] T050 [US1] Add input box styles to chat.css (textarea, send button, character counter)

### Frontend: API Integration (US1 Backend Connection)

- [X] T051 [US1] Update ChatWidget to import useDocusaurusContext and read customFields.ragApiUrl from Docusaurus config
- [X] T052 [US1] Implement sendMessage() function in ChatWidget using axios to POST /api/chat/query with query, history (empty for now), selected_text (null for now)
- [X] T053 [US1] Handle API responses in ChatWidget (append user message and assistant response to messages state, update isLoading)
- [X] T054 [US1] Implement error handling in ChatWidget for API failures (display user-friendly error message "Chatbot temporarily unavailable")
- [X] T055 [US1] Add loading indicator in ChatWidget (typing animation or spinner while isLoading is true)

### Frontend: Docusaurus Integration (US1 Deployment)

- [X] T056 [US1] Create physical-ai-humanoid-robotics/src/theme/Root.js to wrap app with ChatWidget component
- [X] T057 [US1] Update physical-ai-humanoid-robotics/docusaurus.config.js to add customFields.ragApiUrl (default: http://localhost:8000)
- [X] T058 [US1] Test chat widget appears on all Docusaurus pages with floating button in bottom-right corner
- [X] T059 [US1] Test full end-to-end flow: click button → open chat → type question → receive response with citations → click citation link → navigate to book section

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Core RAG functionality (indexing, query processing, response generation, citations) works end-to-end.

---

## Phase 4: User Story 2 - Context-Specific Text Explanation (Priority: P2)

**Goal**: Enable readers to highlight text in the book, click "Ask about this text," and request simplified explanations. The chatbot provides context-aware responses focused on the highlighted content.

**Independent Test**: Highlight any paragraph in the book, click the context action, ask questions like "Simplify this" or "Give me an example," and verify the response directly addresses the selected text with relevant explanations.

### Frontend: Text Selection Detection (US2 Core)

- [ ] T060 [P] [US2] Create physical-ai-humanoid-robotics/src/components/chat/TextSelectionHandler.jsx with event listeners for mouseup and touchend to detect text selection
- [ ] T061 [US2] Implement selection state management in TextSelectionHandler (store selected text and bounding rect using window.getSelection())
- [ ] T062 [US2] Add floating tooltip in TextSelectionHandler positioned near selection with "Ask about this text" button
- [ ] T063 [US2] Add tooltip styles to chat.css (fixed position, transform for centering, z-index, hover effect)

### Frontend: Text Selection Integration (US2 Connection)

- [ ] T064 [US2] Integrate TextSelectionHandler into ChatWidget to receive onTextSelected callback with selected text
- [ ] T065 [US2] Update ChatWidget state to store selectedText from TextSelectionHandler
- [ ] T066 [US2] Update ChatWidget UI to display "Asking about: [truncated text]" when selectedText is present
- [ ] T067 [US2] Update sendMessage() in ChatWidget to include selected_text in API request when available
- [ ] T068 [US2] Clear selectedText from state after message is sent

### Backend: Selected Text Handling (US2 Logic)

- [ ] T069 [US2] Update rag_service.py process_query() to detect when selected_text is provided (Mode B query)
- [ ] T070 [US2] Modify prompt engineering in rag_service.py to prioritize selected_text as context when present (add to beginning of prompt)
- [ ] T071 [US2] Adjust Qdrant search in rag_service.py for Mode B: reduce top-N to 3-5 chunks when selected_text provides primary context
- [ ] T072 [US2] Test Mode B queries: submit query with selected_text and verify response focuses on highlighted content (e.g., "Simplify this" with complex paragraph)

### Frontend: Mode B User Experience (US2 Polish)

- [ ] T073 [US2] Add visual indicator in ChatWidget when operating in Mode B (selected text mode) vs Mode A (full book mode)
- [ ] T074 [US2] Implement "Clear selection" option in ChatWidget to reset to Mode A
- [ ] T075 [US2] Test cross-browser compatibility of text selection detection (Chrome, Firefox, Safari, Edge)
- [ ] T076 [US2] Test text selection on mobile/tablet viewports with touch events

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Readers can use both Mode A (full book search) and Mode B (selected text queries).

---

## Phase 5: User Story 3 - Multi-Turn Conversation with Memory (Priority: P3)

**Goal**: Enable readers to have extended conversations about complex topics with the chatbot remembering previous questions and answers. Supports up to 10 consecutive exchanges within a session.

**Independent Test**: Conduct a multi-turn conversation (e.g., asking "What is NVIDIA Isaac?" followed by "How do I set it up?" followed by "Show me an example workflow") and verify that later responses reference earlier parts of the conversation with contextual understanding.

### Backend: Conversation History Handling (US3 Core Logic)

- [ ] T077 [US3] Update rag_service.py process_query() to accept history parameter (List[ChatMessage] with max 10 messages)
- [ ] T078 [US3] Implement sliding window in rag_service.py to keep only last 10 exchanges if history exceeds limit
- [ ] T079 [US3] Update prompt engineering in rag_service.py to include conversation history (format: "User: X\nAssistant: Y\n")
- [ ] T080 [US3] Test multi-turn conversation via API: send 3 sequential queries with cumulative history and verify context preservation (e.g., "What is ROS 2?" → "How do I install it?" → "Show me an example")

### Frontend: History State Management (US3 State)

- [ ] T081 [US3] Update ChatWidget messages state to store full conversation history (array of ChatMessage objects with role, content, sources)
- [ ] T082 [US3] Update sendMessage() in ChatWidget to pass messages as history in API request (convert to format expected by backend)
- [ ] T083 [US3] Implement history persistence in browser sessionStorage to survive page navigation within same session
- [ ] T084 [US3] Implement history loading from sessionStorage on ChatWidget mount
- [ ] T085 [US3] Implement "Clear conversation" button in ChatWidget header to reset history

### Frontend: Conversation Memory UX (US3 Polish)

- [ ] T086 [US3] Update MessageList to show full conversation history with timestamps
- [ ] T087 [US3] Add auto-scroll in MessageList to latest message when new message arrives
- [ ] T088 [US3] Add conversation context indicator in ChatWidget (e.g., "3 messages in conversation")
- [ ] T089 [US3] Test conversation persistence: navigate between book pages and verify history persists in same browser session
- [ ] T090 [US3] Test new session behavior: open new browser tab/window and verify conversation resets

**Checkpoint**: All user stories (US1, US2, US3) should now be independently functional. Readers can use full book search, selected text queries, and have multi-turn conversations with memory.

---

## Phase 6: User Story 4 - Feedback and Improvement (Priority: P4)

**Goal**: Enable readers to provide feedback (thumbs up/down + optional comment) on chatbot responses. Feedback is logged in Neon Postgres for quality monitoring and continuous improvement.

**Independent Test**: Submit positive/negative feedback on responses and verify that feedback is logged with the query, response, rating, comment, and timestamp in the database.

### Frontend: Feedback Buttons (US4 UI)

- [ ] T091 [P] [US4] Create physical-ai-humanoid-robotics/src/components/chat/FeedbackButtons.jsx with thumbs up/down buttons
- [ ] T092 [US4] Implement feedback submission UI in FeedbackButtons (thumbs down opens optional comment textarea)
- [ ] T093 [US4] Add feedback button styles to chat.css (button styling, textarea for comment, max 1000 characters)

### Frontend: Feedback Integration (US4 Connection)

- [ ] T094 [US4] Integrate FeedbackButtons into MessageList for each assistant message
- [ ] T095 [US4] Implement submitFeedback() function in ChatWidget using axios to POST /api/chat/feedback with FeedbackRequest (query, response, selected_text, rating, comment, session_id, sources)
- [ ] T096 [US4] Generate session_id in ChatWidget on mount (use UUID or simple timestamp-based ID, store in sessionStorage)
- [ ] T097 [US4] Handle feedback submission success (show "Thank you for feedback!" message, disable feedback buttons for that message)
- [ ] T098 [US4] Handle feedback submission errors (show error message, allow retry)

### Backend: Feedback Storage (US4 Backend)

- [ ] T099 [P] [US4] Create rag-backend/app/services/neon_service.py with store_feedback() method to insert feedback into Neon Postgres using SQLAlchemy
- [ ] T100 [US4] Create rag-backend/app/routers/chat.py POST /api/chat/feedback endpoint accepting FeedbackRequest
- [ ] T101 [US4] Implement /api/chat/feedback endpoint calling neon_service.store_feedback() and returning success message with feedback_id
- [ ] T102 [US4] Add error handling in /api/chat/feedback for database connection errors (500), validation errors (400)
- [ ] T103 [US4] Test feedback endpoint with Postman/curl (submit positive and negative feedback) and verify data is stored in Neon Postgres feedback table

### Feedback Data Validation (US4 Quality)

- [ ] T104 [US4] Query Neon Postgres feedback table and verify all feedback records have required fields (query, response, rating, timestamp)
- [ ] T105 [US4] Test feedback with comment (verify comment is stored correctly, max 1000 characters enforced)
- [ ] T106 [US4] Test feedback with selected_text (Mode B) and verify selected_text is stored
- [ ] T107 [US4] Test feedback with sources (verify sources_json is stored as JSONB array)

**Checkpoint**: All user stories (US1, US2, US3, US4) are now complete. Full RAG chatbot functionality is available including feedback collection.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements, error handling, and documentation that affect multiple user stories

### Error Handling & Edge Cases

- [ ] T108 [P] Implement query length validation in ChatWidget (max 2000 characters, show warning)
- [ ] T109 [P] Implement selected text length validation in TextSelectionHandler (max 1000 words, truncate or prompt for smaller selection)
- [ ] T110 [P] Handle concurrent requests in ChatWidget (disable send button during processing, queue or show "Please wait" message)
- [ ] T111 [P] Handle API unavailability in ChatWidget (display "Chatbot temporarily unavailable" message, allow retrying)
- [ ] T112 Handle rate limit errors (429) from Gemini API in gemini_service.py with exponential backoff (already implemented, verify working)
- [ ] T113 Handle out-of-scope queries in rag_service.py (when Qdrant returns no results above threshold, return "Topic not covered in book" message)
- [ ] T114 Handle special characters and code snippets in queries (ensure proper escaping in rag_service.py prompt assembly)
- [ ] T115 Handle non-English queries in rag_service.py (detect language, return polite "English only" message)

### Performance Optimization

- [ ] T116 [P] Verify Qdrant search latency <200ms (test with sample queries, optimize HNSW parameters if needed)
- [ ] T117 [P] Verify total query response time <3s (measure end-to-end from API request to response, optimize bottlenecks)
- [ ] T118 [P] Optimize frontend bundle size (code-split ChatWidget for lazy loading on first open)
- [ ] T119 Test concurrent users (simulate 10+ concurrent requests, verify no performance degradation)

### Accessibility & Responsive Design

- [X] T120 [P] Test keyboard navigation in ChatWidget (tab order, Enter to send, Escape to close)
- [X] T121 [P] Test screen reader compatibility (ARIA labels, semantic HTML, announce new messages)
- [X] T122 [P] Test responsive design on mobile viewports (<768px) - chat should be full-width modal on small screens
- [X] T123 [P] Test responsive design on tablet viewports (768-1024px) - chat should adapt to available space
- [X] T124 Test cross-browser compatibility (Chrome, Firefox, Safari, Edge - verify UI renders correctly, functionality works)

### Documentation & Deployment Readiness

- [ ] T125 [P] Create rag-backend/README.md with backend setup instructions, API documentation, deployment guide
- [ ] T126 [P] Update physical-ai-humanoid-robotics/README.md (if exists) to mention RAG chatbot integration
- [ ] T127 [P] Create deployment documentation for backend (Railway/Render setup, environment variables, health checks)
- [ ] T128 [P] Create deployment documentation for frontend (Vercel deployment, update customFields.ragApiUrl to production URL)
- [ ] T129 Verify all environment variables are documented in .env.example with correct format and descriptions
- [ ] T130 Run quickstart.md validation (follow all setup steps from scratch, verify they work)

### Code Quality & Linting

- [ ] T131 [P] Run black on rag-backend/app/ to format Python code (PEP 8 compliance)
- [ ] T132 [P] Run flake8 on rag-backend/app/ and fix any linting issues
- [ ] T133 [P] Run mypy on rag-backend/app/ to check type hints (fix any type errors)
- [ ] T134 [P] Review and clean up console.log statements in frontend components (remove debug logs)
- [ ] T135 [P] Add JSDoc comments to complex functions in frontend components (ChatWidget, RAG service methods)

### Admin & Maintenance

- [ ] T136 [US1] Implement POST /api/index/refresh endpoint in admin.py to trigger book content re-indexing
- [ ] T137 [US1] Test /api/index/refresh endpoint (trigger re-indexing, verify Qdrant collection is recreated with updated content)
- [ ] T138 Create simple script to query Neon Postgres feedback table for admin review (rag-backend/scripts/view_feedback.py)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T010) - **BLOCKS all user stories**
- **User Story 1 (Phase 3)**: Depends on Foundational completion (T011-T022)
- **User Story 2 (Phase 4)**: Depends on Foundational completion (T011-T022) - Can start in parallel with US1 but builds on US1 components
- **User Story 3 (Phase 5)**: Depends on Foundational completion (T011-T022) - Can start in parallel with US1/US2 but builds on US1 components
- **User Story 4 (Phase 6)**: Depends on Foundational completion (T011-T022) - Can start in parallel with other user stories
- **Polish (Phase 7)**: Depends on desired user stories being complete (at minimum US1 for MVP)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - **No dependencies on other stories** - This is the MVP
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - **Builds on US1** (uses ChatWidget, sendMessage, API endpoint) but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - **Builds on US1** (uses ChatWidget, messages state, API endpoint) but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - **Builds on US1** (uses MessageList, API structure) but is completely independent functionality

### Within Each User Story

**User Story 1 (P1)**:
1. Content Indexing (T023-T027) - Must complete before RAG Service
2. RAG Service (T028-T032) - Must complete before Query API
3. Query API (T033-T038) - Must complete before Frontend Integration
4. Frontend components can be built in parallel: Chat Button (T039-T040), Message List (T045-T047), Input Box (T048-T050)
5. Chat Widget Container (T041-T044) integrates all components
6. API Integration (T051-T055) connects frontend to backend
7. Docusaurus Integration (T056-T059) deploys everything

**User Story 2 (P2)**:
1. Text Selection Detection (T060-T063) can be built in parallel with US1
2. Text Selection Integration (T064-T068) requires ChatWidget from US1
3. Backend handling (T069-T072) requires rag_service from US1
4. Mode B UX (T073-T076) is final polish

**User Story 3 (P3)**:
1. Backend History Handling (T077-T080) requires rag_service from US1
2. Frontend History State (T081-T085) requires ChatWidget from US1
3. Conversation Memory UX (T086-T090) is final integration

**User Story 4 (P4)**:
1. Frontend Feedback Buttons (T091-T093) can be built in parallel
2. Feedback Integration (T094-T098) requires ChatWidget and MessageList from US1
3. Backend Feedback Storage (T099-T103) can be built in parallel with frontend
4. Validation (T104-T107) tests end-to-end

### Parallel Opportunities

**Phase 1 (Setup)** - All tasks marked [P] can run in parallel:
- T002, T003, T005, T006, T007, T008, T010

**Phase 2 (Foundational)** - Tasks marked [P] can run in parallel:
- T013, T014, T020 (after T011-T012 complete)

**Phase 3 (User Story 1)** - Parallel opportunities:
- T023, T024 (chunking and embedding utils)
- T028, T029 (Gemini and Qdrant services)
- T039, T040 (Chat Button)
- T045, T048 (Message List and Input Box)

**Across User Stories** - Once Foundational phase completes:
- All user stories (US1, US2, US3, US4) can start in parallel if team capacity allows
- Different team members can work on different user stories simultaneously
- US1 is priority; others build on it but add independent value

---

## Parallel Example: User Story 1

```bash
# Launch parallel tasks for backend services:
Task T028: "Create rag-backend/app/services/gemini_service.py with generate_embedding() and generate_response() methods"
Task T029: "Create rag-backend/app/services/qdrant_service.py with search() method"

# Launch parallel tasks for frontend components:
Task T039: "Create physical-ai-humanoid-robotics/src/components/chat/ChatButton.jsx"
Task T045: "Create physical-ai-humanoid-robotics/src/components/chat/MessageList.jsx"
Task T048: "Create physical-ai-humanoid-robotics/src/components/chat/InputBox.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - Recommended Approach

1. Complete Phase 1: Setup (T001-T010) - ~30 minutes
2. Complete Phase 2: Foundational (T011-T022) - ~2-3 hours
3. Complete Phase 3: User Story 1 (T023-T059) - ~1-2 days
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Index book content (verify 500-1000 chunks in Qdrant)
   - Ask sample questions from each module
   - Verify responses include accurate answers with citations
   - Test citation links navigate to correct book sections
   - Measure response time (<3s target)
5. Deploy/demo if ready

**MVP Deliverable**: Readers can ask questions about any book content and receive citation-backed answers via a floating chat widget. This is the core value proposition.

### Incremental Delivery (All User Stories)

1. Complete Setup + Foundational (T001-T022) → Foundation ready
2. Add User Story 1 (T023-T059) → Test independently → Deploy/Demo **MVP!**
3. Add User Story 2 (T060-T076) → Test independently → Deploy/Demo (adds selected text queries)
4. Add User Story 3 (T077-T090) → Test independently → Deploy/Demo (adds conversation memory)
5. Add User Story 4 (T091-T107) → Test independently → Deploy/Demo (adds feedback collection)
6. Polish (T108-T138) → Final refinements and deployment prep
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T022)
2. **Once Foundational is done, split work**:
   - **Developer A**: User Story 1 (T023-T059) - Priority, blocks others
   - **Developer B**: User Story 4 (T091-T107) - Can work independently in parallel
   - **Developer C**: Start on error handling and polish (T108-T115)
3. **After US1 completes**:
   - **Developer A**: User Story 2 (T060-T076)
   - **Developer B**: User Story 3 (T077-T090)
   - **Developer C**: Continue polish tasks
4. **Integration and final testing** (all developers)

---

## Task Summary

**Total Tasks**: 138

**Tasks per User Story**:
- Setup (Phase 1): 10 tasks
- Foundational (Phase 2): 12 tasks
- User Story 1 - Full Book Search (Phase 3): 37 tasks 🎯 MVP
- User Story 2 - Context-Specific Text (Phase 4): 17 tasks
- User Story 3 - Multi-Turn Conversation (Phase 5): 14 tasks
- User Story 4 - Feedback and Improvement (Phase 6): 17 tasks
- Polish & Cross-Cutting (Phase 7): 31 tasks

**Parallel Opportunities Identified**: 41 tasks marked [P]

**Independent Test Criteria**:
- **US1**: Ask questions from different modules, verify citation-backed responses, test end-to-end flow
- **US2**: Highlight text, ask contextual questions, verify responses focus on selected content
- **US3**: Conduct multi-turn conversation, verify context preservation across 3-4 exchanges
- **US4**: Submit feedback, verify storage in database with all required fields

**Suggested MVP Scope**: User Story 1 only (T001-T059) = **59 tasks total for MVP**

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability (US1, US2, US3, US4)
- Each user story should be independently completable and testable
- Commit after each task or logical group of related tasks
- Stop at any checkpoint to validate story independently
- MVP is User Story 1 - delivers core RAG functionality and immediate value
- User Stories 2-4 add enhancements but are optional for initial launch
- Tests are NOT included as they were not requested in the specification
- All file paths are absolute from repository root for clarity
- Follow quickstart.md for setup instructions and development workflow
- Refer to plan.md, data-model.md, and contracts/openapi.yaml for implementation details
