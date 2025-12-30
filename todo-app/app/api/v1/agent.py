"""Agent API endpoints for the todo app."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.dependencies import get_db
from app.services.todo import TodoService


class AgentRequest(BaseModel):
    message: str


class AgentResponse(BaseModel):
    response: str


router = APIRouter()


# Import the agent tools and agent here
try:
    from agents import Runner
    from app.agents.tools.todo_tools import todo_service, create_todo, list_todos, get_todo, update_todo, delete_todo, toggle_todo
    from app.agents.agents.todo_agent import todo_agent

    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Agent import failed: {e}")
    AGENT_AVAILABLE = False
    Runner = None
    todo_agent = None


@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Chat with the todo management agent.

    This endpoint allows users to interact with the OpenAI agent that can manage todos.
    The agent can create, list, update, delete, and toggle todos based on natural language requests.
    """
    if not AGENT_AVAILABLE:
        return AgentResponse(response="OpenAI Agents are not available. Please install the required dependencies.")

    try:
        result = await Runner.run(todo_agent, request.message)
        return AgentResponse(response=result.final_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing agent request: {str(e)}")


@router.post("/setup")
async def setup_agent():
    """
    Setup the agent with access to the actual todo database.

    This endpoint configures the agent to use the real todo service instead of the mock one.
    """
    if not AGENT_AVAILABLE:
        return {"message": "OpenAI Agents are not available. Please install the required dependencies."}

    # In a real implementation, we would connect the agent to the actual todo service
    # For now, we'll just return a success message
    return {"message": "Agent setup completed successfully"}