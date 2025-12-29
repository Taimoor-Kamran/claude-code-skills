"""API v1 router."""
from fastapi import APIRouter

from app.api.v1 import todos

router = APIRouter()

router.include_router(todos.router, prefix="/todos", tags=["todos"])
