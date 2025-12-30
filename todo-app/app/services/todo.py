from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.todo import TodoRepository
from app.models.todo import Todo as TodoModel, Priority
from app.schemas.todo import TodoCreate, TodoUpdate, Todo, TodoList


class TodoService:
    def __init__(self, session: AsyncSession):
        self.repository = TodoRepository(session)

    async def create_todo(self, todo_data: TodoCreate) -> Todo:
        todo = await self.repository.create(
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed,
            priority=todo_data.priority.value if isinstance(todo_data.priority, Priority) else todo_data.priority,
            due_date=todo_data.due_date
        )
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
        priority_str = priority.value if priority else None
        todos, total = await self.repository.get_all(
            skip=skip,
            limit=limit,
            search=search,
            completed=completed,
            priority=priority_str,
            date_from=date_from,
            date_to=date_to,
        )
        return TodoList(
            todos=[Todo.model_validate(todo) for todo in todos],
            total=total,
        )

    async def update_todo(self, todo_id: int, todo_data: TodoUpdate) -> Todo:
        update_data = todo_data.model_dump(exclude_unset=True)
        # Convert priority enum to string if needed
        if "priority" in update_data and update_data["priority"]:
            update_data["priority"] = update_data["priority"].value if isinstance(update_data["priority"], Priority) else update_data["priority"]

        todo = await self.repository.update(todo_id, **update_data)
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
