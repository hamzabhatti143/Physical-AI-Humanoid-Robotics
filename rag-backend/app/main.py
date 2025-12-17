"""FastAPI application for RAG Chatbot."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for Physical AI & Humanoid Robotics book chatbot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "RAG Chatbot API is running", "version": "1.0.0"}


# Include routers
from app.routers import admin, chat

app.include_router(admin.router, prefix="/api", tags=["admin"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
