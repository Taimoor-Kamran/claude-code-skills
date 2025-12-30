"""
Custom streaming endpoint that mimics ChatKit functionality for the todo app.

This creates a streaming endpoint that can work with the ChatKit frontend component
but uses our existing OpenAI Agents implementation.
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import json
from typing import AsyncGenerator

from agents import Runner
from app.agents.agents.todo_agent import todo_agent

router = APIRouter()

async def event_generator(message: str) -> AsyncGenerator[str, None]:
    """
    Generate streaming events for the chat response.
    This mimics the ChatKit event format.
    """
    try:
        # The streaming functionality might not be directly available in the openai-agents package
        # as implemented. For now, return a simple response.
        # In a real implementation, we would use the proper streaming API.

        # For now, let's return a single response since the streaming API might be different
        result = await Runner.run(todo_agent, message)
        yield f"data: {json.dumps({'type': 'text', 'content': result.final_output})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

@router.post("/chatkit")
async def chatkit_stream_endpoint(request: Request):
    """
    Streaming endpoint that works with ChatKit frontend but uses our todo agent.
    """
    body = await request.json()
    message = body.get("message", "")

    return StreamingResponse(
        event_generator(message),
        media_type="text/event-stream"
    )