"""Main FastAPI application integrating todo app and OpenAI agents."""

from contextlib import asynccontextmanager
import os
from fastapi import FastAPI

# Import the original todo app
from app.main import app as todo_app
from app.core.config import settings

# Import the agent API
from src.todo_agents.api.agent_api import router as agent_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    yield
    # Shutdown


# Create the main application
app = FastAPI(
    title="Todo App with AI Agents",
    version="0.1.0",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Include the original todo API routes
app.include_router(todo_app.router, prefix="/api/v1", tags=["todos"])

# Include the agent API routes
app.include_router(agent_router, prefix="/api/v1", tags=["agent"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "todo-app-with-agents"}


# Export the app for use with uvicorn
if __name__ != "__main__":
    # This allows the original todo app to be used independently
    pass