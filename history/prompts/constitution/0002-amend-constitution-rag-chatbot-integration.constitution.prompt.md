---
id: 0002
title: Amend Constitution RAG Chatbot Integration
stage: constitution
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Hamza Bhatti
command: /sp.constitution
labels: ["constitution", "rag-chatbot", "governance", "principles"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Manual validation of constitution structure
  - Template consistency verification
---

## Prompt

Create governing principles for RAG Chatbot integration with existing "Physical AI & Humanoid Robotics" Docusaurus book:

1. **Technical Quality Standards:**
   - RAG chatbot uses Gemini API (Google AI)
   - FastAPI backend (separate service)
   - Neon Serverless Postgres for metadata
   - Qdrant Cloud Free Tier for embeddings
   - Frontend integrated into existing Docusaurus site at physical-ai-humanoid-robotics/

2. **Project Integration:**
   - Backend in new rag-backend/ folder at root level
   - Frontend components in physical-ai-humanoid-robotics/src/components/chat/
   - No changes to existing book content structure
   - Chat widget accessible on all documentation pages

3. **Architecture:**
   - Backend API: localhost:8000 (development)
   - Frontend: embedded in Docusaurus
   - CORS enabled for Docusaurus origin
   - Environment variables in backend/.env

4. **User Experience:**
   - Floating chat button on all pages
   - Two modes: full book query + selected text query
   - Citation links to book sections

## Response snapshot

Updated constitution from v1.0.0 to v1.1.0 with four new principle sections:

1. **RAG Chatbot Integration Standards**: Defines technical requirements for Gemini API, FastAPI backend, Neon Postgres, and Qdrant vector database. Mandates citation-backed responses.

2. **Project Structure and Integration**: Establishes folder structure (rag-backend/ for backend, physical-ai-humanoid-robotics/src/components/chat/ for frontend) and separation of concerns.

3. **Development Architecture**: Specifies localhost:8000 for development, CORS configuration, .env usage for secrets, health check endpoints, and RESTful API conventions.

4. **User Experience and Accessibility**: Requires floating chat button, dual query modes (full book + selected text), clickable citations, keyboard/screen-reader accessibility, and responsive design.

Also expanded existing Technical Guidelines to include explicit MUST requirements for Python/PEP 8, .env usage, and secret management.

## Outcome

- ✅ Impact: Constitution version 1.1.0 created with comprehensive RAG chatbot governance
- 🧪 Tests: Manual validation of structure and completeness
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Create feature specification (/sp.specify), then architectural plan (/sp.plan)
- 🧠 Reflection: MINOR version bump appropriate as new principles are additive and non-breaking. Existing templates require no updates since principles don't conflict with current structure.

## Evaluation notes (flywheel)

- Failure modes observed: None detected during constitution update
- Graders run and results (PASS/FAIL): Structure validation PASS, placeholder check PASS, routing validation PASS
- Prompt variant (if applicable): Standard constitution amendment flow
- Next experiment (smallest change to try): Validate constitution principles during spec creation to ensure compliance
