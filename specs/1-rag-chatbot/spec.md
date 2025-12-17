# Feature Specification: RAG Chatbot for Physical AI & Humanoid Robotics Book

**Feature Branch**: `1-rag-chatbot`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "Build RAG chatbot for existing 'Physical AI & Humanoid Robotics' Docusaurus book in robotic/ folder"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full Book Search and Query (Priority: P1)

A reader exploring the Physical AI & Humanoid Robotics book wants quick answers to specific technical questions without manually searching through all modules. They can ask natural language questions about any topic covered in the book and receive accurate answers with citations pointing to relevant sections.

**Why this priority**: This is the core RAG functionality that delivers immediate value. Without this, the chatbot cannot serve its primary purpose of helping readers find information quickly.

**Independent Test**: Can be fully tested by asking questions about content from different modules (e.g., "What is ROS 2?", "How does NVIDIA Isaac work?") and verifying that responses include accurate information with proper source citations. Delivers value by reducing reader search time from minutes to seconds.

**Acceptance Scenarios**:

1. **Given** a reader is on any page of the Docusaurus book, **When** they click the floating chat button, **Then** a chat interface opens where they can type questions
2. **Given** the chat interface is open, **When** the reader types "Explain ROS 2 nodes" and submits, **Then** the system retrieves relevant content from Module 1, generates a comprehensive answer, and displays citations with clickable links to the source sections
3. **Given** a reader asks a question about content in Module 3, **When** the response is generated, **Then** the citations include the module name, section title, and URL that links directly to that content
4. **Given** a reader asks a follow-up question, **When** they submit it, **Then** the system uses conversation history to provide contextually aware answers
5. **Given** a reader asks about a topic not covered in the book, **When** the system cannot find relevant content, **Then** it clearly states that the topic is not covered in the available material

---

### User Story 2 - Context-Specific Text Explanation (Priority: P2)

A reader encounters a complex paragraph or technical concept in Module 3 that they don't fully understand. They can highlight the text, click "Ask about this text," and request simplified explanations or deeper clarification about that specific content.

**Why this priority**: This enhances the learning experience by providing on-demand explanations for difficult concepts. It builds on P1 by adding context-aware queries, making the chatbot more intelligent and helpful.

**Independent Test**: Can be tested by highlighting any paragraph in the book, clicking the context action, asking questions like "Simplify this" or "Give me an example," and verifying the response directly addresses the selected text. Delivers value by providing personalized explanations without requiring the reader to formulate complex queries.

**Acceptance Scenarios**:

1. **Given** a reader is viewing content in any module, **When** they highlight a paragraph of text, **Then** a "Ask about this text" action appears near the selection
2. **Given** a reader has highlighted text and clicked the action, **When** the chat interface opens, **Then** the selected text is automatically included as context for the query
3. **Given** selected text is provided as context, **When** the reader types "Simplify this," **Then** the system generates an explanation specific to the highlighted content without searching the entire book
4. **Given** a reader asks for examples related to highlighted text, **When** the response is generated, **Then** it provides relevant examples that directly relate to the selected passage
5. **Given** a reader highlights text from one section and asks a question, **When** the system responds, **Then** the answer focuses on the selected text while optionally referencing related content from other sections

---

### User Story 3 - Multi-Turn Conversation with Memory (Priority: P3)

A reader wants to have an extended conversation about a complex topic like "NVIDIA Isaac Sim workflow," asking multiple related questions in sequence. The chatbot remembers previous questions and answers to provide increasingly detailed and contextually relevant responses.

**Why this priority**: This creates a more natural learning experience similar to having a conversation with an instructor. While valuable, it depends on P1 and P2 being functional first.

**Independent Test**: Can be tested by conducting a multi-turn conversation (e.g., asking "What is NVIDIA Isaac?" followed by "How do I set it up?" followed by "Show me an example workflow") and verifying that later responses reference earlier parts of the conversation. Delivers value by enabling deeper exploration without repetition.

**Acceptance Scenarios**:

1. **Given** a reader has asked about "ROS 2 nodes," **When** they follow up with "How do they communicate?", **Then** the system understands the context refers to ROS 2 nodes and provides relevant information about inter-node communication
2. **Given** a conversation has progressed through 3-4 exchanges, **When** the reader asks a clarifying question, **Then** the system maintains context from all previous exchanges in that session
3. **Given** a reader closes the chat interface, **When** they reopen it in the same browser session, **Then** the conversation history persists and they can continue from where they left off
4. **Given** a reader starts a new browser session, **When** they open the chat, **Then** the conversation history resets and they start fresh
5. **Given** a long conversation with many exchanges, **When** the reader asks a new unrelated question, **Then** the system can shift context appropriately without being overly constrained by earlier topics

---

### User Story 4 - Feedback and Improvement (Priority: P4)

A reader receives an answer that is inaccurate or unhelpful. They can provide feedback (thumbs up/down) to help improve the system's responses over time. This feedback is logged for review and potential model refinement.

**Why this priority**: This enables continuous improvement and quality monitoring. It's valuable for long-term maintenance but not essential for initial launch.

**Independent Test**: Can be tested by submitting positive/negative feedback on responses and verifying that feedback is logged with the query, response, and timestamp. Delivers value by creating a feedback loop for quality assurance.

**Acceptance Scenarios**:

1. **Given** a reader receives a response, **When** they see thumbs up/down buttons below the message, **Then** they can click one to provide feedback
2. **Given** a reader clicks thumbs down, **When** prompted, **Then** they can optionally provide additional written feedback explaining the issue
3. **Given** feedback is submitted, **When** it's sent to the backend, **Then** it's stored with the query, response, selected text (if any), timestamp, and user feedback text
4. **Given** an administrator wants to review feedback, **When** they access the feedback logs [NEEDS CLARIFICATION: Will there be an admin dashboard or direct database access for reviewing feedback?], **Then** they can see all submitted feedback with context
5. **Given** multiple readers provide feedback on similar queries, **When** patterns emerge, **Then** the data can inform content improvements or model fine-tuning

---

### Edge Cases

- **What happens when the backend API is unavailable?** The chat interface should display a user-friendly error message like "The chatbot is temporarily unavailable. Please try again later." and allow the reader to continue browsing the book normally.

- **How does the system handle very long questions (>1000 characters)?** The system should accept questions up to 2000 characters and truncate with a warning if exceeded, ensuring queries remain focused and processable.

- **What if a reader highlights more than 1000 words of text?** The system should use only the first 1000 words as context or prompt the reader to select a smaller section, preventing token limit issues.

- **How does the system handle concurrent requests from the same user?** Only one query should be processed at a time per user session; additional requests should be queued or the UI should disable the send button until the current response completes.

- **What if the book content is updated after indexing?** The admin can trigger a re-indexing operation via the /api/index/refresh endpoint to update the vector database with new content.

- **How does the system handle special characters or code snippets in queries?** The system should properly escape and handle all UTF-8 characters, code blocks, and markdown formatting without breaking.

- **What if the conversation history becomes very long (>20 exchanges)?** The system should maintain a sliding window of the most recent 10 exchanges to stay within token limits while preserving context.

- **How does the system handle questions in languages other than English?** The system is designed for English content and queries. Non-English queries should return a polite message indicating the chatbot currently supports English only.

## Requirements *(mandatory)*

### Functional Requirements

#### Core Chat Functionality
- **FR-001**: System MUST provide a persistent floating chat button visible on all Docusaurus pages in the bottom-right corner
- **FR-002**: System MUST open a chat interface (modal or sidebar) when the chat button is clicked
- **FR-003**: System MUST accept natural language queries from readers up to 2000 characters in length
- **FR-004**: System MUST display a message history showing all questions and answers in the current session
- **FR-005**: System MUST provide visual indicators (e.g., typing animation) while processing queries

#### Content Retrieval & RAG
- **FR-006**: System MUST index all content from the physical-ai-humanoid-robotics/docs/ directory, including all four modules (module-1-ros2, module-2-digital-twin, module-3-nvidia-isaac, module-4-vla)
- **FR-007**: System MUST chunk content into semantic sections of 500-1000 tokens, preserving context boundaries (paragraphs, sections)
- **FR-008**: System MUST generate embeddings using Gemini's text-embedding-004 model (768 dimensions)
- **FR-009**: System MUST store embeddings in Qdrant Cloud vector database with metadata including chunk_id, module, section, title, url, and content
- **FR-010**: System MUST retrieve the most relevant content chunks (top 5-10) based on semantic similarity to the user's query
- **FR-011**: System MUST use retrieved chunks as context for Gemini's generative model to produce accurate, contextual answers

#### Query Modes
- **FR-012**: System MUST support Mode A (Full Book Query) where queries search across all indexed book content
- **FR-013**: System MUST support Mode B (Selected Text Query) where queries use highlighted text as additional context
- **FR-014**: System MUST detect when selected_text is provided and prioritize it in the response generation
- **FR-015**: System MUST maintain conversation history within a session to support multi-turn conversations with context awareness

#### Response & Citations
- **FR-016**: System MUST generate responses that are accurate, informative, and grounded in the book content
- **FR-017**: System MUST include source citations for all responses, showing module name, section title, and clickable URL
- **FR-018**: System MUST format citations as an array of source objects containing module, section, and url fields
- **FR-019**: System MUST render citations in the chat interface as clickable links that navigate to the referenced book section

#### Text Selection Integration
- **FR-020**: System MUST detect when a reader highlights text on any Docusaurus page
- **FR-021**: System MUST display an "Ask about this text" action button near the highlighted text
- **FR-022**: System MUST open the chat interface with the selected text pre-loaded as context when the action is triggered
- **FR-023**: System MUST preserve the selected text as part of the query payload sent to the backend API

#### Feedback Mechanism
- **FR-024**: System MUST display thumbs up/down buttons below each chatbot response
- **FR-025**: System MUST allow readers to optionally provide written feedback when they click thumbs down
- **FR-026**: System MUST send feedback data (query, response, selected_text, rating, comment, timestamp) to the backend for logging
- **FR-027**: System MUST store feedback in Neon Postgres database for later review and analysis

#### API Endpoints
- **FR-028**: Backend MUST expose POST /api/chat/query endpoint accepting query, history, and optional selected_text
- **FR-029**: Backend MUST expose POST /api/chat/feedback endpoint accepting feedback data
- **FR-030**: Backend MUST expose GET /api/health endpoint returning system health status
- **FR-031**: Backend MUST expose POST /api/index/refresh endpoint to trigger re-indexing of book content
- **FR-032**: Backend MUST enable CORS for http://localhost:3000 during development and production domain when deployed

#### Indexing & Data Management
- **FR-033**: System MUST provide a script (index_book_content.py) that reads markdown files from ../physical-ai-humanoid-robotics/docs/
- **FR-034**: System MUST parse markdown content, extract titles, headings, and body text for indexing
- **FR-035**: System MUST generate metadata for each chunk including unique chunk_id, module path, section name, title, and URL path
- **FR-036**: System MUST support incremental re-indexing when book content is updated via the /api/index/refresh endpoint
- **FR-037**: System MUST log indexing operations including number of chunks processed, success/failure status, and errors

#### Integration & Configuration
- **FR-038**: Docusaurus MUST integrate the chat widget via src/theme/Root.js without modifying existing book content
- **FR-039**: Docusaurus config MUST include customFields.ragApiUrl pointing to the backend API (default: http://localhost:8000)
- **FR-040**: Frontend MUST use axios library to make HTTP requests to the backend API
- **FR-041**: Frontend MUST read ragApiUrl from Docusaurus config and use it for all API calls
- **FR-042**: Backend MUST read configuration from environment variables including GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DATABASE_URL, and BOOK_CONTENT_PATH

#### Error Handling
- **FR-043**: System MUST display user-friendly error messages when the backend is unavailable or requests fail
- **FR-044**: System MUST handle rate limiting from Gemini API gracefully, queuing requests or showing "Please wait" messages
- **FR-045**: System MUST validate user input to prevent injection attacks or malformed queries
- **FR-046**: System MUST log all errors with sufficient detail for debugging (request ID, timestamp, error type, stack trace)
- **FR-047**: System MUST return appropriate HTTP status codes (200 OK, 400 Bad Request, 500 Internal Server Error, 503 Service Unavailable)

### Key Entities

- **ChatMessage**: Represents a single message in the conversation with attributes: message_id, role (user/assistant), content (text), timestamp, sources (array of citations), feedback (optional)

- **Chunk**: Represents a piece of indexed book content with attributes: chunk_id (unique identifier like "m1_w3_c1"), module (e.g., "module-1-ros2"), section (e.g., "week-3-fundamentals"), title (e.g., "ROS 2 Architecture"), url (relative path like "/module-1-ros2/week-3-fundamentals"), content (actual text, 500-1000 tokens), embedding (768-dimensional vector)

- **Source**: Represents a citation linking a response to book content with attributes: module (module name), section (section/chapter name), url (clickable link to content), relevance_score (optional, for ranking)

- **Feedback**: Represents user feedback on a response with attributes: feedback_id (unique), query (original question), response (chatbot answer), selected_text (context if provided), rating (thumbs up/down or 1-5 scale), comment (optional written feedback), timestamp, session_id (optional for grouping)

- **QueryRequest**: API request payload with attributes: query (user question string), history (array of previous messages for context), selected_text (optional highlighted content)

- **QueryResponse**: API response payload with attributes: response (generated answer string), sources (array of Source objects with module, section, url)

- **IndexingJob**: Represents a content indexing operation with attributes: job_id (unique), status (running/completed/failed), start_time, end_time, chunks_processed (count), errors (array of error messages)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Readers can receive relevant answers to book-related queries in under 3 seconds (95th percentile response time)
- **SC-002**: System achieves 90% accuracy in retrieving relevant book content for queries, measured by precision of top-5 retrieved chunks
- **SC-003**: 80% of user queries result in responses that include at least one valid citation linking back to book content
- **SC-004**: The chat interface is accessible and functional on desktop browsers (Chrome, Firefox, Safari, Edge) and maintains Docusaurus theme consistency
- **SC-005**: System handles at least 50 concurrent users during development/testing without performance degradation
- **SC-006**: Conversation context is preserved for at least 10 consecutive exchanges within a single session
- **SC-007**: Selected text queries (Mode B) produce responses that are 90% focused on the highlighted content, measured by relevance scoring
- **SC-008**: Indexing script successfully processes all four book modules (100+ markdown files) in under 10 minutes
- **SC-009**: 95% of API requests complete successfully without errors under normal operating conditions
- **SC-010**: System integrates with existing Docusaurus book without breaking navigation, search, or any existing functionality

## Dependencies *(mandatory)*

### External Services
- **Gemini API**: Required for embedding generation (text-embedding-004) and response generation (gemini-1.5-flash or similar)
- **Qdrant Cloud**: Vector database for storing and retrieving embeddings
- **Neon Postgres**: Relational database for storing feedback and metadata
- **Docusaurus**: Existing book platform that must remain fully functional

### Technical Dependencies
- **FastAPI**: Python web framework for backend API
- **Axios**: JavaScript HTTP client for frontend API calls
- **React**: Required by Docusaurus, used for chat components
- **Node.js & npm**: For running and building Docusaurus

### Assumptions
- The existing Docusaurus book content in physical-ai-humanoid-robotics/docs/ is well-structured markdown with clear headings and sections
- The Gemini API key provided has sufficient quota for development and testing workloads
- Qdrant Cloud and Neon Postgres services are accessible and have sufficient storage capacity
- The book content is primarily in English
- Readers access the book via modern web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- Internet connectivity is available for API calls to Gemini, Qdrant, and Neon
- The development environment supports Python 3.9+ and Node.js 18+

## Constraints *(mandatory)*

### Technical Constraints
- Must not modify existing book content in physical-ai-humanoid-robotics/docs/
- Must maintain Docusaurus theme consistency and styling
- Backend must be separate from Docusaurus (in rag-backend/ folder)
- Must use specified versions: Gemini text-embedding-004 (768d), Qdrant Cloud, Neon Postgres
- Frontend changes limited to src/components/chat/, src/theme/Root.js, docusaurus.config.js, and package.json
- CORS must allow http://localhost:3000 for development

### Operational Constraints
- Embedding generation and storage costs must be monitored to stay within Gemini API free tier or allocated budget
- Response generation must complete in under 5 seconds to maintain user engagement
- The chat interface must not obstruct critical book navigation or content

### Security Constraints
- API keys and database credentials must be stored in environment variables, never hardcoded
- User queries must be validated to prevent injection attacks
- The system must not expose sensitive information (API keys, database connection strings) in client-side code
- Feedback data should not include personally identifiable information unless explicitly required

### Scope Constraints (Out of Scope)
- User authentication and account management
- Voice-based queries or text-to-speech responses
- Multi-language support (only English)
- Integration with external data sources beyond the book content
- Real-time collaboration or multi-user chat sessions
- Mobile app versions (web-only)
- Advanced analytics dashboard for administrators (basic feedback logging only)

## Open Questions

1. **Feedback Review Mechanism**: Will administrators access feedback via a dedicated admin dashboard, direct database queries, or exported reports? *(P4 implementation detail, can be decided during planning phase)*

**Assumption for now**: Feedback will be stored in Neon Postgres and administrators will query the database directly using SQL or a basic query tool. A dedicated admin dashboard is out of scope for the initial implementation.
