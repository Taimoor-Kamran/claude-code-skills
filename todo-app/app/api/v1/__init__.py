"""API v1 router."""
from fastapi import APIRouter

from app.api.v1 import todos
from app.api.v1 import agent

router = APIRouter()

router.include_router(todos.router, prefix="/todos", tags=["todos"])
router.include_router(agent.router, prefix="/agent", tags=["agent"])
