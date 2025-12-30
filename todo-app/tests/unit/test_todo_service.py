import pytest
from datetime import datetime
from fastapi import HTTPException, status
from app.models.todo import Priority
from app.schemas.todo import TodoCreate, TodoUpdate
from app.services.todo import TodoService


class TestTodoService:
    """Test cases for TodoService."""

    @pytest.mark.asyncio
    async def test_create_todo(self, db_session):
        """Test creating a todo through the service."""
        service = TodoService(db_session)

        todo_data = TodoCreate(
            title="Test Todo",
            description="Test Description",
            priority=Priority.HIGH,
            due_date=datetime(2025, 12, 31)
        )

        created_todo = await service.create_todo(todo_data)

        assert created_todo.title == "Test Todo"
        assert created_todo.description == "Test Description"
        assert created_todo.priority == Priority.HIGH
        assert created_todo.due_date == datetime(2025, 12, 31)
        assert created_todo.completed is False
        assert created_todo.id is not None

    @pytest.mark.asyncio
    async def test_get_todo(self, db_session, created_todo):
        """Test getting a todo by ID."""
        service = TodoService(db_session)

        retrieved_todo = await service.get_todo(created_todo.id)

        assert retrieved_todo.id == created_todo.id
        assert retrieved_todo.title == created_todo.title
        assert retrieved_todo.description == created_todo.description

    @pytest.mark.asyncio
    async def test_get_todo_not_found(self, db_session):
        """Test getting a non-existent todo raises HTTPException."""
        service = TodoService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            await service.get_todo(999)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_list_todos(self, db_session):
        """Test listing todos."""
        service = TodoService(db_session)

        # Create multiple todos
        await service.create_todo(TodoCreate(
            title="Todo 1",
            description="Description 1",
            priority=Priority.LOW
        ))
        await service.create_todo(TodoCreate(
            title="Todo 2",
            description="Description 2",
            priority=Priority.HIGH
        ))

        result = await service.list_todos()

        assert len(result.todos) == 2
        assert result.total == 2
        assert result.todos[0].title == "Todo 2"  # Ordered by created_at desc
        assert result.todos[1].title == "Todo 1"

    @pytest.mark.asyncio
    async def test_list_todos_with_filters(self, db_session):
        """Test listing todos with filters."""
        service = TodoService(db_session)

        # Create todos with different attributes
        await service.create_todo(TodoCreate(
            title="High Priority Todo",
            priority=Priority.HIGH,
            completed=False
        ))
        await service.create_todo(TodoCreate(
            title="Completed Todo",
            priority=Priority.MEDIUM,
            completed=True
        ))
        await service.create_todo(TodoCreate(
            title="Low Priority Todo",
            priority=Priority.LOW,
            completed=False
        ))

        # Test priority filter
        result = await service.list_todos(priority=Priority.HIGH)
        assert result.total >= 1
        if result.todos:
            assert result.todos[0].priority == Priority.HIGH

        # Test completion filter - check we have at least one completed todo
        result = await service.list_todos(completed=True)
        assert result.total >= 1  # Should have at least 1 completed todo
        if result.todos:
            assert result.todos[0].completed is True

        # Test completion filter for non-completed todos
        result = await service.list_todos(completed=False)
        assert result.total >= 2  # Should have at least 2 non-completed todos

        # Test search filter
        result = await service.list_todos(search="High Priority")
        assert result.total == 1
        assert "High Priority" in result.todos[0].title

    @pytest.mark.asyncio
    async def test_update_todo(self, db_session, created_todo):
        """Test updating a todo."""
        service = TodoService(db_session)

        update_data = TodoUpdate(
            title="Updated Todo",
            description="Updated Description",
            priority=Priority.HIGH,
            completed=True
        )

        updated_todo = await service.update_todo(created_todo.id, update_data)

        assert updated_todo.id == created_todo.id
        assert updated_todo.title == "Updated Todo"
        assert updated_todo.description == "Updated Description"
        assert updated_todo.priority == Priority.HIGH
        assert updated_todo.completed is True

    @pytest.mark.asyncio
    async def test_update_todo_not_found(self, db_session):
        """Test updating a non-existent todo raises HTTPException."""
        service = TodoService(db_session)

        update_data = TodoUpdate(title="Updated Todo")

        with pytest.raises(HTTPException) as exc_info:
            await service.update_todo(999, update_data)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_delete_todo(self, db_session, created_todo):
        """Test deleting a todo."""
        service = TodoService(db_session)

        # Verify todo exists before deletion
        todo_before = await service.get_todo(created_todo.id)
        assert todo_before is not None

        # Delete the todo
        await service.delete_todo(created_todo.id)

        # Verify todo no longer exists
        with pytest.raises(HTTPException) as exc_info:
            await service.get_todo(created_todo.id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_todo_not_found(self, db_session):
        """Test deleting a non-existent todo raises HTTPException."""
        service = TodoService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            await service.delete_todo(999)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_toggle_complete(self, db_session, created_todo):
        """Test toggling todo completion status."""
        service = TodoService(db_session)

        # Verify initial state
        initial_todo = await service.get_todo(created_todo.id)
        assert initial_todo.completed is False

        # Toggle completion
        toggled_todo = await service.toggle_complete(created_todo.id)

        assert toggled_todo.id == created_todo.id
        assert toggled_todo.completed is True

        # Toggle again
        toggled_todo2 = await service.toggle_complete(created_todo.id)

        assert toggled_todo2.id == created_todo.id
        assert toggled_todo2.completed is False

    @pytest.mark.asyncio
    async def test_toggle_complete_not_found(self, db_session):
        """Test toggling completion for non-existent todo raises HTTPException."""
        service = TodoService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            await service.toggle_complete(999)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_list_todos_pagination(self, db_session):
        """Test pagination of todos."""
        service = TodoService(db_session)

        # Create 5 todos
        for i in range(5):
            await service.create_todo(TodoCreate(
                title=f"Todo {i+1}",
                priority=Priority.MEDIUM
            ))

        # Get first 2 todos
        result = await service.list_todos(skip=0, limit=2)
        assert len(result.todos) == 2
        assert result.total == 5

        # Get next 2 todos
        result = await service.list_todos(skip=2, limit=2)
        assert len(result.todos) == 2
        assert result.total == 5

    @pytest.mark.asyncio
    async def test_create_todo_with_minimal_data(self, db_session):
        """Test creating a todo with minimal required data."""
        service = TodoService(db_session)

        todo_data = TodoCreate(title="Minimal Todo")

        created_todo = await service.create_todo(todo_data)

        assert created_todo.title == "Minimal Todo"
        assert created_todo.description is None
        assert created_todo.priority == Priority.MEDIUM  # Default priority
        assert created_todo.due_date is None
        assert created_todo.completed is False