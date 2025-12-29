from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.schemas.todo import Todo, TodoCreate, TodoUpdate, TodoList, Priority
from app.services.todo import TodoService

router = APIRouter()


async def get_todo_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TodoService:
    return TodoService(db)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    service: TodoServiceDep,
) -> Todo:
    """Create a new todo item."""
    return await service.create_todo(todo_data)


@router.get("/", response_model=TodoList)
async def list_todos(
    service: TodoServiceDep,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    search: str | None = Query(None, description="Search in title and description"),
    completed: bool | None = Query(None, description="Filter by completion status"),
    priority: Priority | None = Query(None, description="Filter by priority level"),
    date_from: datetime | None = Query(None, description="Filter by due date (from)"),
    date_to: datetime | None = Query(None, description="Filter by due date (to)"),
) -> TodoList:
    """
    List all todos with optional filters.

    - **search**: Search in title and description
    - **completed**: Filter by completion status (true/false)
    - **priority**: Filter by priority (low, medium, high)
    - **date_from**: Filter todos with due date >= this date
    - **date_to**: Filter todos with due date <= this date
    """
    return await service.list_todos(
        skip=skip,
        limit=limit,
        search=search,
        completed=completed,
        priority=priority,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: int,
    service: TodoServiceDep,
) -> Todo:
    """Get a specific todo by ID."""
    return await service.get_todo(todo_id)


@router.patch("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    service: TodoServiceDep,
) -> Todo:
    """Update a todo item."""
    return await service.update_todo(todo_id, todo_data)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    service: TodoServiceDep,
) -> None:
    """Delete a todo item."""
    await service.delete_todo(todo_id)


@router.post("/{todo_id}/toggle", response_model=Todo)
async def toggle_todo_complete(
    todo_id: int,
    service: TodoServiceDep,
) -> Todo:
    """Toggle the completion status of a todo."""
    return await service.toggle_complete(todo_id)
