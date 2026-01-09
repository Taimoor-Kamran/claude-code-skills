"""API endpoints for OpenAI Agent integration."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agents import Runner
from src.todo_agents.agents.todo_agent import todo_agent


router = APIRouter()


class AgentRequest(BaseModel):
    message: str


class AgentResponse(BaseModel):
    response: str


@router.post("/agent/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Chat with the todo management agent.

    This endpoint allows users to interact with the OpenAI agent that can manage todos.
    The agent can create, list, update, delete, and toggle todos based on natural language requests.
    """
    try:
        result = await Runner.run(todo_agent, request.message)
        return AgentResponse(response=result.final_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing agent request: {str(e)}")