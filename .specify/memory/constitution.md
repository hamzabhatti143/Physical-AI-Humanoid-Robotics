<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles:
- Technical Guidelines (expanded for RAG integration)
Added sections:
- RAG Chatbot Integration Standards (new principle)
- Project Structure and Integration (new principle)
- Development Architecture (new principle)
- User Experience and Accessibility (new principle)
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ no update needed (principles are additive)
- .specify/templates/spec-template.md: ✅ no update needed (principles are additive)
- .specify/templates/tasks-template.md: ✅ no update needed (principles are additive)
- .specify/templates/commands/*.md: ✅ no update needed (principles are additive)
- Runtime guidance docs (e.g., README.md): ⚠ pending (should document RAG integration)
Follow-up TODOs:
- Update root README.md to document RAG chatbot architecture and setup
- Create backend setup documentation once implementation begins
-->
# Physical AI & Humanoid Robotics Constitution

## Core Principles

### Content Quality Standards
- Technical accuracy in AI, robotics, ROS 2, Gazebo, Unity, and NVIDIA Isaac concepts.
- Clear explanations suitable for students transitioning from digital AI to physical embodied intelligence.
- Balance between theoretical foundations and practical implementation.
- Consistency in terminology across all modules (ROS 2, URDF, VSLAM, VLA, etc.).

### Educational Structure
- Progressive learning path from fundamentals to capstone project.
- Each module builds upon previous knowledge.
- Hands-on exercises and real-world applications emphasized.
- Weekly breakdown aligned with quarter schedule (13 weeks).

### Technical Guidelines
- Code examples MUST use Python with rclpy for ROS 2 integration.
- Simulation examples MUST demonstrate Gazebo and Unity workflows.
- NVIDIA Isaac platform integration MUST be clearly documented.
- Voice-to-Action and LLM integration patterns MUST be demonstrated.
- All Python code MUST follow PEP 8 style guidelines.
- Environment-specific configurations MUST use `.env` files; secrets MUST NEVER be committed.

### RAG Chatbot Integration Standards
- RAG chatbot MUST use Gemini API (Google AI) for natural language understanding.
- Backend MUST be implemented as a separate FastAPI service for modularity and scalability.
- Neon Serverless Postgres MUST be used for storing document metadata and query history.
- Qdrant Cloud Free Tier MUST be used for vector embeddings storage and semantic search.
- The chatbot MUST provide accurate, citation-backed answers from the documentation.
- All chatbot responses MUST include direct links to source material in the book.

Rationale: A RAG chatbot enhances learning by allowing students to query the documentation conversationally while maintaining source attribution. Using managed services (Gemini, Neon, Qdrant) minimizes operational overhead while providing production-grade capabilities.

### Project Structure and Integration
- Backend code MUST reside in `rag-backend/` folder at repository root, isolated from frontend.
- Frontend chat components MUST be placed in `physical-ai-humanoid-robotics/src/components/chat/`.
- Existing book content structure MUST NOT be modified during RAG integration.
- Chat widget MUST be accessible on all documentation pages via consistent UI placement.
- Backend and frontend MUST be independently deployable and testable.

Rationale: Clear separation of concerns ensures the chatbot can be developed, tested, and maintained independently without disrupting the existing Docusaurus content. This also allows for future migration or replacement of either component.

### Development Architecture
- Backend API MUST run on `localhost:8000` during local development.
- Frontend MUST be embedded within the existing Docusaurus application.
- CORS MUST be properly configured to allow requests from the Docusaurus origin.
- All sensitive configuration (API keys, database credentials) MUST be stored in `rag-backend/.env`.
- The backend MUST expose a health check endpoint for monitoring and deployment validation.
- API endpoints MUST follow RESTful conventions and return consistent JSON responses.

Rationale: Standard development practices ensure the system is maintainable, secure, and follows industry best practices for API design and secret management.

### User Experience and Accessibility
- A floating chat button MUST be visible and accessible on all documentation pages.
- The chatbot MUST support two query modes:
  1. Full book query: Search across all documentation content.
  2. Selected text query: Context-aware queries based on user-highlighted text.
- All chat responses MUST include clickable citation links to the relevant book sections.
- The chat interface MUST be keyboard-accessible and screen-reader friendly.
- Loading states and error messages MUST be clear and actionable.
- The chat widget MUST be responsive and work on mobile, tablet, and desktop viewports.

Rationale: Accessibility and user experience are paramount for an educational tool. Multiple query modes accommodate different learning styles, while citations ensure academic integrity and allow students to dive deeper into source material.

## Governance
This constitution supersedes all other practices and decisions in the project. Any amendments to this constitution MUST be documented with rationale, require explicit approval, and include a migration plan for affected code and documentation. All pull requests and code reviews MUST verify compliance with these principles. Introduction of complexity MUST be justified against these principles and documented via Architecture Decision Records (ADRs) when architecturally significant.

**Amendment Process**:
1. Proposed changes MUST be submitted via pull request with clear rationale.
2. Changes MUST include impact analysis on existing code and templates.
3. Version MUST be incremented according to semantic versioning:
   - MAJOR: Backward-incompatible governance changes or principle removals.
   - MINOR: New principles added or existing principles materially expanded.
   - PATCH: Clarifications, typo fixes, or non-semantic refinements.
4. All stakeholders MUST review and approve before merge.

**Compliance Review**:
- All feature specifications MUST reference applicable constitution principles.
- All architectural plans MUST demonstrate alignment with technical guidelines.
- Violations MUST be flagged during code review and resolved before merge.

**Version**: 1.1.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-15
