# Quickstart Guide: RAG Chatbot Development

**Feature**: 1-rag-chatbot
**Date**: 2025-12-15
**Purpose**: Step-by-step setup, development, and testing instructions

## Prerequisites

### Required Software

- **Python 3.11+**: For backend development
  ```bash
  python --version  # Should show 3.11 or higher
  ```

- **Node.js 18+**: For Docusaurus frontend
  ```bash
  node --version  # Should show 18.x or higher
  npm --version
  ```

- **Git**: For version control
  ```bash
  git --version
  ```

### Required Accounts & API Keys

1. **Gemini API Key** (Google AI)
   - Sign up at: https://makersuite.google.com/app/apikey
   - Free tier: 15 RPM, 1M TPM, 1500 RPD
   - Copy API key for `.env` file

2. **Qdrant Cloud Account**
   - Sign up at: https://cloud.qdrant.io/
   - Create cluster (Free tier: 1GB storage)
   - Get cluster URL and API key from dashboard

3. **Neon Postgres Account**
   - Sign up at: https://neon.tech/
   - Create project (Free tier: serverless)
   - Get connection string from dashboard

### Project Structure

Ensure you're in the correct directory:
```bash
cd /path/to/robotic  # Repository root
git checkout 1-rag-chatbot  # Feature branch
```

---

## Part 1: Backend Setup

### Step 1: Create Backend Directory Structure

```bash
# From repository root (robotic/)
mkdir -p rag-backend/app/{routers,services,models,utils}
mkdir -p rag-backend/scripts
mkdir -p rag-backend/tests/{test_routers,test_services,test_utils}
touch rag-backend/app/__init__.py
touch rag-backend/app/routers/__init__.py
touch rag-backend/app/services/__init__.py
touch rag-backend/app/models/__init__.py
touch rag-backend/app/utils/__init__.py
```

### Step 2: Create Python Virtual Environment

```bash
cd rag-backend

# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate

# Verify activation (prompt should show (venv))
which python  # Should point to venv/bin/python
```

### Step 3: Install Dependencies

Create `requirements.txt`:
```bash
cat > requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
google-generativeai==0.3.2
qdrant-client==1.7.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.25
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
httpx==0.26.0
tenacity==8.2.3
tiktoken==0.5.2
python-frontmatter==1.0.0
EOF
```

Create `requirements-dev.txt`:
```bash
cat > requirements-dev.txt << 'EOF'
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
black==24.1.1
flake8==7.0.0
mypy==1.8.0
httpx==0.26.0
EOF
```

Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 4: Configure Environment Variables

Create `.env` file:
```bash
cat > .env << 'EOF'
# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant Cloud
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Neon Postgres
NEON_DATABASE_URL=your_neon_connection_string_here

# Book Content Path
BOOK_CONTENT_PATH=../physical-ai-humanoid-robotics/docs

# CORS
ALLOWED_ORIGINS=http://localhost:3000
EOF
```

**Replace placeholder values with your actual credentials.**

Create `.env.example` (for version control):
```bash
cat > .env.example << 'EOF'
# Gemini API
GEMINI_API_KEY=AIzaSy...

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key

# Neon Postgres
NEON_DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Book Content Path
BOOK_CONTENT_PATH=../physical-ai-humanoid-robotics/docs

# CORS
ALLOWED_ORIGINS=http://localhost:3000
EOF
```

### Step 5: Create Configuration Module

Create `app/config.py`:
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    gemini_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    neon_database_url: str
    book_content_path: str = "../physical-ai-humanoid-robotics/docs"
    allowed_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
```

### Step 6: Create FastAPI Application

Create `app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="RAG Chatbot API",
    description="API for Physical AI & Humanoid Robotics book chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}

# Import routers (will add later)
# from app.routers import chat, admin
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(admin.router, prefix="/api", tags=["admin"])
```

### Step 7: Test Backend Server

```bash
# Start server (from rag-backend/)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, test
curl http://localhost:8000/
# Should return: {"message":"RAG Chatbot API is running"}
```

---

## Part 2: Database Setup

### Step 8: Create Neon Postgres Table

Create `scripts/setup_database.py`:
```python
import psycopg2
from app.config import settings

def create_feedback_table():
    conn = psycopg2.connect(settings.neon_database_url)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
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

        CREATE INDEX IF NOT EXISTS idx_feedback_timestamp ON feedback(timestamp);
        CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback(rating);
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Feedback table created successfully")

if __name__ == "__main__":
    create_feedback_table()
```

Run setup:
```bash
cd rag-backend
python scripts/setup_database.py
```

### Step 9: Create Qdrant Collection

Create `scripts/setup_qdrant.py`:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config import settings

def create_collection():
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )

    # Delete if exists (for clean setup)
    try:
        client.delete_collection("book_chunks")
        print("🗑️  Deleted existing collection")
    except Exception:
        pass

    # Create new collection
    client.create_collection(
        collection_name="book_chunks",
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        ),
        optimizers_config={
            "indexing_threshold": 10000
        },
        hnsw_config={
            "m": 16,
            "ef_construct": 100
        }
    )

    print("✅ Qdrant collection 'book_chunks' created successfully")

if __name__ == "__main__":
    create_collection()
```

Run setup:
```bash
python scripts/setup_qdrant.py
```

---

## Part 3: Frontend Setup

### Step 10: Navigate to Docusaurus Project

```bash
# From repository root
cd physical-ai-humanoid-robotics
```

### Step 11: Install Axios Dependency

```bash
# Check if axios is already installed
cat package.json | grep axios

# If not present, add it
npm install axios@^1.6.0

# Verify installation
npm list axios
```

### Step 12: Create Chat Components Directory

```bash
mkdir -p src/components/chat
```

### Step 13: Create Minimal Chat Button Component

Create `src/components/chat/ChatButton.jsx`:
```jsx
import React from 'react';
import './chat.css';

export default function ChatButton({ onClick }) {
  return (
    <button className="chat-button" onClick={onClick}>
      💬
    </button>
  );
}
```

Create `src/components/chat/chat.css`:
```css
.chat-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--ifm-color-primary);
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: transform 0.2s;
}

.chat-button:hover {
  transform: scale(1.1);
}
```

### Step 14: Create Minimal Chat Widget

Create `src/components/chat/ChatWidget.jsx`:
```jsx
import React, { useState } from 'react';
import ChatButton from './ChatButton';
import './chat.css';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <ChatButton onClick={() => setIsOpen(!isOpen)} />
      {isOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <h3>Ask about the book</h3>
            <button onClick={() => setIsOpen(false)}>✕</button>
          </div>
          <div className="chat-body">
            <p>Chat interface coming soon...</p>
          </div>
        </div>
      )}
    </>
  );
}
```

Update `src/components/chat/chat.css`:
```css
/* ... existing button styles ... */

.chat-container {
  position: fixed;
  bottom: 100px;
  right: 20px;
  width: 400px;
  height: 500px;
  background: var(--ifm-background-color);
  border: 1px solid var(--ifm-color-emphasis-300);
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--ifm-color-emphasis-300);
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
}

.chat-header button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.chat-body {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}
```

### Step 15: Integrate Chat Widget in Docusaurus

Create `src/theme/Root.js`:
```jsx
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

### Step 16: Update Docusaurus Config

Edit `docusaurus.config.js`:
```javascript
// Find the module.exports section and add customFields
module.exports = {
  // ... existing config ...

  customFields: {
    ragApiUrl: process.env.RAG_API_URL || 'http://localhost:8000'
  },

  // ... rest of config ...
};
```

### Step 17: Test Frontend

```bash
# Start Docusaurus dev server (from physical-ai-humanoid-robotics/)
npm start

# Browser should open to http://localhost:3000
# You should see a floating chat button in bottom-right corner
# Click it to open the chat interface (placeholder for now)
```

---

## Part 4: End-to-End Testing

### Step 18: Test Backend Health Endpoint

First, implement the health endpoint in `app/routers/admin.py`:
```python
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "qdrant": "connected",  # TODO: implement actual checks
            "postgres": "connected",
            "gemini": "connected"
        },
        "version": "1.0.0"
    }
```

Update `app/main.py`:
```python
# ... existing imports ...
from app.routers import admin

# ... existing app setup ...

app.include_router(admin.router, prefix="/api", tags=["admin"])
```

Test:
```bash
# Start backend (Terminal 1)
cd rag-backend
uvicorn app.main:app --reload

# Test health endpoint (Terminal 2)
curl http://localhost:8000/api/health

# Should return:
# {
#   "status": "healthy",
#   "timestamp": "2025-12-15T...",
#   "services": {...},
#   "version": "1.0.0"
# }
```

### Step 19: Test CORS from Frontend

Update `ChatWidget.jsx` to test API connection:
```jsx
import React, { useState, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import axios from 'axios';
import ChatButton from './ChatButton';
import './chat.css';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking...');
  const {siteConfig} = useDocusaurusContext();
  const apiUrl = siteConfig.customFields.ragApiUrl;

  useEffect(() => {
    // Test API connection
    axios.get(`${apiUrl}/api/health`)
      .then(response => {
        setApiStatus(`✅ Connected (v${response.data.version})`);
      })
      .catch(error => {
        setApiStatus(`❌ Connection failed: ${error.message}`);
      });
  }, [apiUrl]);

  return (
    <>
      <ChatButton onClick={() => setIsOpen(!isOpen)} />
      {isOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <h3>Ask about the book</h3>
            <button onClick={() => setIsOpen(false)}>✕</button>
          </div>
          <div className="chat-body">
            <p><strong>API Status:</strong> {apiStatus}</p>
            <p>Chat interface coming soon...</p>
          </div>
        </div>
      )}
    </>
  );
}
```

Test:
```bash
# Terminal 1: Backend running (from rag-backend/)
uvicorn app.main:app --reload

# Terminal 2: Frontend running (from physical-ai-humanoid-robotics/)
npm start

# Open http://localhost:3000
# Click chat button
# Should see "✅ Connected (v1.0.0)" in chat widget
```

---

## Part 5: Development Workflow

### Daily Development

1. **Start Backend**:
   ```bash
   cd rag-backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend** (separate terminal):
   ```bash
   cd physical-ai-humanoid-robotics
   npm start
   ```

3. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs
   - Backend health check: http://localhost:8000/api/health

### Running Tests

```bash
# Backend tests (from rag-backend/)
pytest tests/ -v

# Backend tests with coverage
pytest tests/ --cov=app --cov-report=html

# Frontend tests (from physical-ai-humanoid-robotics/)
npm test
```

### Code Formatting

```bash
# Backend (from rag-backend/)
black app/ scripts/ tests/  # Format code
flake8 app/ scripts/ tests/  # Lint code

# Frontend (from physical-ai-humanoid-robotics/)
npm run format  # If configured
```

---

## Part 6: Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution**: Ensure you're in `rag-backend/` directory and virtual environment is activated.
```bash
cd rag-backend
source venv/bin/activate
which python  # Should show venv/bin/python
```

### Issue: CORS error in browser console

**Symptom**: "Access-Control-Allow-Origin" error when frontend calls backend.

**Solution**: Check CORS configuration:
1. Verify `.env` has `ALLOWED_ORIGINS=http://localhost:3000`
2. Restart backend server
3. Check browser console for actual error details

### Issue: Gemini API "PERMISSION_DENIED"

**Solution**: Verify API key is correct and has billing enabled (if required).
```bash
# Test API key
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=YOUR_API_KEY"
```

### Issue: Qdrant connection timeout

**Solution**: Check cluster URL and API key.
```python
# Test connection (Python)
from qdrant_client import QdrantClient
client = QdrantClient(url="YOUR_URL", api_key="YOUR_KEY")
print(client.get_collections())  # Should list collections
```

### Issue: Neon Postgres connection refused

**Solution**: Verify connection string includes `sslmode=require`.
```bash
# Test connection (from rag-backend/)
python -c "import psycopg2; from app.config import settings; conn = psycopg2.connect(settings.neon_database_url); print('✅ Connected'); conn.close()"
```

### Issue: Chat button not appearing

**Solution**: Check Docusaurus console for errors.
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Verify `src/theme/Root.js` exists
4. Restart dev server (`npm start`)

---

## Part 7: Next Steps

After completing this quickstart:

1. ✅ Backend server running
2. ✅ Frontend with chat button integrated
3. ✅ Databases configured (Qdrant, Neon Postgres)
4. ✅ API health check working
5. ✅ CORS configured and tested

**Ready for Implementation**:
- Run `/sp.tasks` to generate detailed task breakdown
- Start with Phase 1 tasks (backend services, Pydantic schemas)
- Implement indexing script to populate Qdrant
- Build RAG service for query processing
- Develop full chat UI components

---

## Quick Reference

### Important Directories

```text
robotic/
├── rag-backend/              # Backend API
│   ├── app/                  # Application code
│   ├── scripts/              # Utility scripts (indexing, setup)
│   ├── tests/                # Backend tests
│   ├── .env                  # Environment variables (DO NOT COMMIT)
│   └── requirements.txt      # Python dependencies
│
└── physical-ai-humanoid-robotics/
    ├── src/
    │   ├── components/chat/  # Chat UI components
    │   └── theme/Root.js     # App wrapper
    ├── docs/                 # Book content (DO NOT MODIFY)
    └── docusaurus.config.js  # Docusaurus config
```

### Key Commands

| Action | Command |
|--------|---------|
| Start backend | `cd rag-backend && uvicorn app.main:app --reload` |
| Start frontend | `cd physical-ai-humanoid-robotics && npm start` |
| Run backend tests | `cd rag-backend && pytest tests/ -v` |
| Format backend code | `cd rag-backend && black app/` |
| Install backend deps | `cd rag-backend && pip install -r requirements.txt` |
| Install frontend deps | `cd physical-ai-humanoid-robotics && npm install` |
| Access API docs | http://localhost:8000/docs |
| Access frontend | http://localhost:3000 |

### Environment Variables

Copy from `.env.example` to `.env` and fill in:
- `GEMINI_API_KEY`: From https://makersuite.google.com/app/apikey
- `QDRANT_URL`: From Qdrant Cloud dashboard
- `QDRANT_API_KEY`: From Qdrant Cloud dashboard
- `NEON_DATABASE_URL`: From Neon dashboard (connection string)

---

## Support

- **OpenAPI Docs**: http://localhost:8000/docs (interactive API testing)
- **Spec**: `specs/1-rag-chatbot/spec.md`
- **Plan**: `specs/1-rag-chatbot/plan.md`
- **Data Model**: `specs/1-rag-chatbot/data-model.md`
- **API Contracts**: `specs/1-rag-chatbot/contracts/openapi.yaml`
