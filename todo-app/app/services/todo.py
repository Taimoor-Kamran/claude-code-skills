from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate, Todo, TodoList, Priority


class TodoService:
    def __init__(self, session: AsyncSession):
        self.repository = TodoRepository(session)

    async def create_todo(self, todo_data: TodoCreate) -> Todo:
        todo = await self.repository.create(todo_data)
        return Todo.model_validate(todo)

    async def get_todo(self, todo_id: int) -> Todo:
        todo = await self.repository.get_by_id(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found",
            )
        return Todo.model_validate(todo)

    async def list_todos(
        self,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        completed: bool | None = None,
        priority: Priority | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> TodoList:
        todos, total = await self.repository.get_all(
            skip=skip,
            limit=limit,
            search=search,
            completed=completed,
            priority=priority,
            date_from=date_from,
            date_to=date_to,
        )
        return TodoList(
            todos=[Todo.model_validate(todo) for todo in todos],
            total=total,
        )

    async def update_todo(self, todo_id: int, todo_data: TodoUpdate) -> Todo:
        todo = await self.repository.update(todo_id, todo_data)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found",
            )
        return Todo.model_validate(todo)

    async def delete_todo(self, todo_id: int) -> None:
        deleted = await self.repository.delete(todo_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found",
            )

    async def toggle_complete(self, todo_id: int) -> Todo:
        todo = await self.repository.toggle_complete(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found",
            )
        return Todo.model_validate(todo)
