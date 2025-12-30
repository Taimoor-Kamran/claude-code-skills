import pytest
from datetime import datetime
from app.models.todo import Todo, Priority


class TestTodoModel:
    """Test cases for Todo model."""

    def test_todo_creation(self):
        """Test creating a todo instance."""
        todo = Todo(
            title="Test Todo",
            description="Test Description",
            priority=Priority.MEDIUM.value,
            due_date=datetime(2025, 12, 31),
            completed=False
        )

        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.priority == Priority.MEDIUM.value
        assert todo.due_date == datetime(2025, 12, 31)
        assert todo.completed is False
        assert todo.id is None  # ID is set by the database

    def test_todo_default_values(self):
        """Test default values for todo."""
        todo = Todo(
            title="Test Todo",
            description="Test Description"
        )

        # In SQLModel, the completed field has a default value of False
        # Priority default is set at DB level, so it may be None when object is created in Python
        assert todo.completed is False  # Default value
        assert todo.priority is None  # Default set at DB level, not at Python object level
        assert todo.created_at is not None  # Created by default_factory
        assert todo.updated_at is not None  # Created by default_factory

    def test_todo_priority_enum(self):
        """Test priority enum values."""
        assert Priority.LOW.value == "low"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.HIGH.value == "high"

    def test_todo_priority_validation(self):
        """Test that priority values are valid."""
        todo = Todo(title="Test", priority=Priority.HIGH.value)
        assert todo.priority in [p.value for p in Priority]

    def test_todo_string_representation(self):
        """Test string representation of todo (if __str__ is implemented)."""
        todo = Todo(title="Test Todo", description="Test Description")
        # Since we don't have a __str__ method, we just check that it's a valid object
        assert isinstance(todo.title, str)
        assert todo.title == "Test Todo"
