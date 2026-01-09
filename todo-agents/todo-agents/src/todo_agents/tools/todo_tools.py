"""Todo management tools for OpenAI Agents."""

import asyncio
from typing import Optional
from datetime import datetime
from agents import function_tool

# Import the todo app components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'todo-app'))

from app.services.todo import TodoService
from app.schemas.todo import TodoCreate, TodoUpdate, Priority
from app.core.database import get_session, engine
from sqlmodel import select
from app.models.todo import Todo as TodoModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class TodoAppService:
    """Wrapper for todo app service to be used with OpenAI agents."""

    def __init__(self):
        # Initialize the database session
        self.engine = engine
        self.SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def create_todo(self, title: str, description: Optional[str] = None,
                         priority: str = "medium", due_date: Optional[str] = None) -> dict:
        """Create a new todo item."""
        try:
            async with self.SessionLocal() as session:
                # Parse due_date if provided
                parsed_due_date = None
                if due_date:
                    try:
                        parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    except ValueError:
                        # If ISO format fails, try other common formats
                        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']:
                            try:
                                parsed_due_date = datetime.strptime(due_date, fmt)
                                break
                            except ValueError:
                                continue

                # Validate priority
                if priority not in ["low", "medium", "high"]:
                    priority = "medium"

                # Create the todo service and use it
                service = TodoService(session)
                todo_data = TodoCreate(
                    title=title,
                    description=description,
                    priority=Priority(priority),
                    due_date=parsed_due_date,
                    completed=False
                )

                todo = await service.create_todo(todo_data)

                # Convert to dict for return
                return todo.model_dump()
        except Exception as e:
            return {"error": f"Failed to create todo: {str(e)}"}

    async def list_todos(self, completed: Optional[bool] = None,
                        priority: Optional[str] = None,
                        search: Optional[str] = None) -> list:
        """List all todo items with optional filters."""
        try:
            async with self.SessionLocal() as session:
                # Create the todo service and use it
                service = TodoService(session)

                # Convert priority string to Priority enum if provided
                priority_enum = None
                if priority:
                    try:
                        priority_enum = Priority(priority)
                    except ValueError:
                        return [{"error": f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'"}]

                result = await service.list_todos(
                    skip=0,
                    limit=100,
                    search=search,
                    completed=completed,
                    priority=priority_enum
                )

                # Convert to list of dicts for return
                return [todo.model_dump() for todo in result.todos]
        except Exception as e:
            return [{"error": f"Failed to list todos: {str(e)}"}]

    async def get_todo(self, todo_id: int) -> Optional[dict]:
        """Get a specific todo by ID."""
        try:
            async with self.SessionLocal() as session:
                # Create the todo service and use it
                service = TodoService(session)

                todo = await service.get_todo(todo_id)
                return todo.model_dump()
        except Exception as e:
            return {"error": f"Failed to get todo: {str(e)}"}

    async def update_todo(self, todo_id: int, title: Optional[str] = None,
                         description: Optional[str] = None,
                         completed: Optional[bool] = None,
                         priority: Optional[str] = None,
                         due_date: Optional[str] = None) -> Optional[dict]:
        """Update a todo item."""
        try:
            async with self.SessionLocal() as session:
                # Parse due_date if provided
                parsed_due_date = None
                if due_date:
                    try:
                        parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    except ValueError:
                        # If ISO format fails, try other common formats
                        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']:
                            try:
                                parsed_due_date = datetime.strptime(due_date, fmt)
                                break
                            except ValueError:
                                continue

                # Validate priority if provided
                priority_enum = None
                if priority:
                    try:
                        priority_enum = Priority(priority)
                    except ValueError:
                        return {"error": f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'"}

                # Create the todo service and use it
                service = TodoService(session)

                # Create update data
                update_data = TodoUpdate(
                    title=title,
                    description=description,
                    completed=completed,
                    priority=priority_enum,
                    due_date=parsed_due_date
                )

                todo = await service.update_todo(todo_id, update_data)
                return todo.model_dump()
        except Exception as e:
            return {"error": f"Failed to update todo: {str(e)}"}

    async def delete_todo(self, todo_id: int) -> dict:
        """Delete a todo item."""
        try:
            async with self.SessionLocal() as session:
                # Create the todo service and use it
                service = TodoService(session)

                await service.delete_todo(todo_id)
                return {"success": True, "message": f"Todo {todo_id} deleted successfully"}
        except Exception as e:
            return {"error": f"Failed to delete todo: {str(e)}"}

    async def toggle_todo(self, todo_id: int) -> Optional[dict]:
        """Toggle the completion status of a todo."""
        try:
            async with self.SessionLocal() as session:
                # Create the todo service and use it
                service = TodoService(session)

                todo = await service.toggle_complete(todo_id)
                return todo.model_dump()
        except Exception as e:
            return {"error": f"Failed to toggle todo: {str(e)}"}


# Create a global instance of the service
todo_service = TodoAppService()


@function_tool
async def create_todo(title: str, description: Optional[str] = None,
                    priority: str = "medium", due_date: Optional[str] = None) -> dict:
    """
    Create a new todo item.

    Args:
        title: The title of the todo (required)
        description: Optional description of the todo
        priority: Priority level - 'low', 'medium', or 'high' (default: 'medium')
        due_date: Optional due date in ISO format (e.g., '2023-12-25' or '2023-12-25T10:30:00')
    """
    return await todo_service.create_todo(title, description, priority, due_date)


@function_tool
async def list_todos(completed: Optional[bool] = None,
                    priority: Optional[str] = None,
                    search: Optional[str] = None) -> list:
    """
    List all todo items with optional filters.

    Args:
        completed: Filter by completion status (True/False)
        priority: Filter by priority ('low', 'medium', 'high')
        search: Search term to match in title or description
    """
    return await todo_service.list_todos(completed, priority, search)


@function_tool
async def get_todo(todo_id: int) -> dict:
    """
    Get a specific todo by ID.

    Args:
        todo_id: The ID of the todo to retrieve
    """
    return await todo_service.get_todo(todo_id)


@function_tool
async def update_todo(todo_id: int, title: Optional[str] = None,
                     description: Optional[str] = None,
                     completed: Optional[bool] = None,
                     priority: Optional[str] = None,
                     due_date: Optional[str] = None) -> dict:
    """
    Update a todo item.

    Args:
        todo_id: The ID of the todo to update
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)
        priority: New priority level (optional)
        due_date: New due date (optional)
    """
    return await todo_service.update_todo(todo_id, title, description, completed, priority, due_date)


@function_tool
async def delete_todo(todo_id: int) -> dict:
    """
    Delete a todo item.

    Args:
        todo_id: The ID of the todo to delete
    """
    return await todo_service.delete_todo(todo_id)


@function_tool
async def toggle_todo(todo_id: int) -> dict:
    """
    Toggle the completion status of a todo.

    Args:
        todo_id: The ID of the todo to toggle
    """
    return await todo_service.toggle_todo(todo_id)