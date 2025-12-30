import pytest
from datetime import datetime
from sqlalchemy import select
from app.models.todo import Todo, Priority
from app.schemas.todo import TodoCreate, TodoUpdate
from app.repositories.todo import TodoRepository


class TestTodoRepository:
    """Test cases for TodoRepository."""

    @pytest.mark.asyncio
    async def test_create_todo(self, db_session):
        """Test creating a todo."""
        repo = TodoRepository(db_session)

        created_todo = await repo.create(
            title="Test Todo",
            description="Test Description",
            priority=Priority.HIGH.value,
            due_date=datetime(2025, 12, 31),
            completed=False
        )

        assert created_todo.title == "Test Todo"
        assert created_todo.description == "Test Description"
        assert created_todo.priority == "high"
        assert created_todo.due_date == datetime(2025, 12, 31)
        assert created_todo.completed is False
        assert created_todo.id is not None

    @pytest.mark.asyncio
    async def test_get_todo_by_id(self, db_session, created_todo):
        """Test getting a todo by ID."""
        repo = TodoRepository(db_session)

        retrieved_todo = await repo.get_by_id(created_todo.id)

        assert retrieved_todo.id == created_todo.id
        assert retrieved_todo.title == created_todo.title
        assert retrieved_todo.description == created_todo.description

    @pytest.mark.asyncio
    async def test_get_todo_by_id_not_found(self, db_session):
        """Test getting a non-existent todo."""
        repo = TodoRepository(db_session)

        retrieved_todo = await repo.get_by_id(999)

        assert retrieved_todo is None

    @pytest.mark.asyncio
    async def test_get_all_todos(self, db_session):
        """Test getting all todos."""
        repo = TodoRepository(db_session)

        # Create multiple todos
        await repo.create(
            title="Todo 1",
            description="Description 1",
            priority=Priority.LOW.value
        )
        await repo.create(
            title="Todo 2",
            description="Description 2",
            priority=Priority.HIGH.value
        )

        todos, total = await repo.get_all()

        assert len(todos) == 2
        assert total == 2
        assert todos[0].title == "Todo 2"  # Should be ordered by created_at desc
        assert todos[1].title == "Todo 1"

    @pytest.mark.asyncio
    async def test_update_todo(self, db_session, created_todo):
        """Test updating a todo."""
        repo = TodoRepository(db_session)

        updated_todo = await repo.update(
            created_todo.id,
            title="Updated Todo",
            description="Updated Description",
            priority=Priority.HIGH.value,
            completed=True
        )

        assert updated_todo.id == created_todo.id
        assert updated_todo.title == "Updated Todo"
        assert updated_todo.description == "Updated Description"
        assert updated_todo.priority == "high"
        assert updated_todo.completed is True

    @pytest.mark.asyncio
    async def test_update_todo_partial(self, db_session, created_todo):
        """Test partially updating a todo."""
        repo = TodoRepository(db_session)

        updated_todo = await repo.update(
            created_todo.id,
            title="Partially Updated"
        )

        assert updated_todo.id == created_todo.id
        assert updated_todo.title == "Partially Updated"
        assert updated_todo.description == created_todo.description  # Unchanged

    @pytest.mark.asyncio
    async def test_update_todo_not_found(self, db_session):
        """Test updating a non-existent todo."""
        repo = TodoRepository(db_session)

        result = await repo.update(999, title="Updated Todo")

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_todo(self, db_session, created_todo):
        """Test deleting a todo."""
        repo = TodoRepository(db_session)

        # Verify todo exists before deletion
        todo_before = await repo.get_by_id(created_todo.id)
        assert todo_before is not None

        # Delete the todo
        result = await repo.delete(created_todo.id)

        assert result is True

        # Verify todo no longer exists
        todo_after = await repo.get_by_id(created_todo.id)
        assert todo_after is None

    @pytest.mark.asyncio
    async def test_delete_todo_not_found(self, db_session):
        """Test deleting a non-existent todo."""
        repo = TodoRepository(db_session)

        result = await repo.delete(999)

        assert result is False

    @pytest.mark.asyncio
    async def test_toggle_complete(self, db_session, created_todo):
        """Test toggling todo completion status."""
        repo = TodoRepository(db_session)

        # Verify initial state
        assert created_todo.completed is False

        # Toggle completion
        toggled_todo = await repo.toggle_complete(created_todo.id)

        assert toggled_todo.id == created_todo.id
        assert toggled_todo.completed is True

        # Toggle again
        toggled_todo2 = await repo.toggle_complete(created_todo.id)

        assert toggled_todo2.id == created_todo.id
        assert toggled_todo2.completed is False

    @pytest.mark.asyncio
    async def test_toggle_complete_not_found(self, db_session):
        """Test toggling completion for non-existent todo."""
        repo = TodoRepository(db_session)

        result = await repo.toggle_complete(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_with_filters(self, db_session):
        """Test filtering todos."""
        repo = TodoRepository(db_session)

        # Create todos with different attributes
        todo1 = await repo.create(
            title="High Priority Todo",
            priority=Priority.HIGH.value,
            completed=False,
            due_date=datetime(2025, 1, 15)
        )

        todo2 = await repo.create(
            title="Completed Todo",
            priority=Priority.MEDIUM.value,
            completed=True
        )

        todo3 = await repo.create(
            title="Low Priority Todo",
            priority=Priority.LOW.value,
            completed=False,
            due_date=datetime(2025, 2, 15)
        )

        # Verify todos were created properly
        assert todo1.completed is False
        assert todo2.completed is True  # This should be True
        assert todo3.completed is False

        # Test priority filter
        todos, total = await repo.get_all(priority=Priority.HIGH.value)
        assert total == 1
        assert todos[0].priority == "high"

        # Test completion filter - check that we have a completed todo
        todos, total = await repo.get_all(completed=True)
        assert total >= 1  # Should have at least 1 completed todo
        if todos:
            assert todos[0].completed is True

        # Test completion filter for non-completed
        todos, total = await repo.get_all(completed=False)
        assert total >= 2  # Should have at least 2 non-completed todos

        # Test search filter
        todos, total = await repo.get_all(search="High Priority")
        assert total == 1
        assert "High Priority" in todos[0].title

        # Test date filter
        todos, total = await repo.get_all(date_from=datetime(2025, 1, 1))
        assert total >= 2  # High priority and Low priority have due dates after Jan 1

        # Test multiple filters
        todos, total = await repo.get_all(completed=False, priority=Priority.LOW.value)
        assert total == 1
        assert todos[0].completed is False
        assert todos[0].priority == "low"

    @pytest.mark.asyncio
    async def test_get_all_pagination(self, db_session):
        """Test pagination of todos."""
        repo = TodoRepository(db_session)

        # Create 5 todos
        for i in range(5):
            await repo.create(
                title=f"Todo {i+1}",
                priority=Priority.MEDIUM.value
            )

        # Get first 2 todos
        todos, total = await repo.get_all(skip=0, limit=2)
        assert len(todos) == 2
        assert total == 5

        # Get next 2 todos
        todos, total = await repo.get_all(skip=2, limit=2)
        assert len(todos) == 2
        assert total == 5

    @pytest.mark.asyncio
    async def test_get_all_search(self, db_session):
        """Test searching todos."""
        repo = TodoRepository(db_session)

        # Create todos with different content
        await repo.create(
            title="Shopping List",
            description="Buy groceries and milk",
            priority=Priority.MEDIUM.value
        )

        await repo.create(
            title="Work Task",
            description="Finish project report",
            priority=Priority.HIGH.value
        )

        await repo.create(
            title="Personal Task",
            description="Call mom",
            priority=Priority.LOW.value
        )

        # Search in title
        todos, total = await repo.get_all(search="Shopping")
        assert total == 1
        assert "Shopping" in todos[0].title

        # Search in description
        todos, total = await repo.get_all(search="groceries")
        assert total == 1
        assert "groceries" in todos[0].description

        # Case insensitive search
        todos, total = await repo.get_all(search="GROCERIES")
        assert total == 1
        assert "groceries" in todos[0].description