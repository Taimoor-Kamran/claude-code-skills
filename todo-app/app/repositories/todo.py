from datetime import datetime

from sqlmodel import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo, Priority


class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, title: str, description: str = None, completed: bool = False,
                    priority: str = Priority.MEDIUM.value, due_date: datetime = None) -> Todo:
        todo = Todo(
            title=title,
            description=description,
            completed=completed,
            priority=priority,
            due_date=due_date
        )
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def get_by_id(self, todo_id: int) -> Todo | None:
        result = await self.session.execute(select(Todo).where(Todo.id == todo_id))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        completed: bool | None = None,
        priority: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> tuple[list[Todo], int]:
        query = select(Todo)
        count_query = select(func.count(Todo.id))

        filters = []

        if search:
            search_filter = or_(
                Todo.title.ilike(f"%{search}%"),
                Todo.description.ilike(f"%{search}%"),
            )
            filters.append(search_filter)

        if completed is not None:
            filters.append(Todo.completed == completed)

        if priority:
            filters.append(Todo.priority == priority)

        if date_from:
            filters.append(Todo.due_date >= date_from)

        if date_to:
            filters.append(Todo.due_date <= date_to)

        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))

        query = query.order_by(Todo.created_at.desc()).offset(skip).limit(limit)

        result = await self.session.execute(query)
        count_result = await self.session.execute(count_query)

        return list(result.scalars().all()), count_result.scalar_one()

    async def update(self, todo_id: int, **kwargs) -> Todo | None:
        todo = await self.get_by_id(todo_id)
        if not todo:
            return None

        for field, value in kwargs.items():
            if hasattr(todo, field):
                setattr(todo, field, value)

        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def delete(self, todo_id: int) -> bool:
        todo = await self.get_by_id(todo_id)
        if not todo:
            return False

        await self.session.delete(todo)
        await self.session.commit()
        return True

    async def toggle_complete(self, todo_id: int) -> Todo | None:
        todo = await self.get_by_id(todo_id)
        if not todo:
            return None

        todo.completed = not todo.completed
        await self.session.commit()
        await self.session.refresh(todo)
        return todo
