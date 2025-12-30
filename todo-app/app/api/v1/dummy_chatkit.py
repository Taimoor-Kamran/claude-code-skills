"""
Dummy ChatKit endpoint for testing frontend functionality.
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import json
import asyncio
from typing import AsyncGenerator

router = APIRouter()

async def dummy_event_generator(message: str) -> AsyncGenerator[str, None]:
    """
    Generate dummy streaming events for testing frontend.
    """
    responses = [
        "I received your message: " + message,
        "Processing your request...",
        "Here's a simulated response from the AI assistant.",
        "This is a dummy response for testing purposes."
    ]

    for response in responses:
        await asyncio.sleep(0.5)  # Simulate processing time
        yield f"data: {json.dumps({'type': 'text', 'content': response})}\n\n"

@router.post("/dummy-chatkit")
async def dummy_chatkit_endpoint(request: Request):
    """
    Dummy ChatKit endpoint for testing frontend functionality.
    """
    body = await request.json()
    message = body.get("message", "Hello")

    return StreamingResponse(
        dummy_event_generator(message),
        media_type="text/event-stream"
    )