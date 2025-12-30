"""Test configuration and fixtures."""
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import ASGITransport, AsyncClient
from datetime import datetime

from app.main import app
from app.core.database import async_session_maker
from app.models.todo import Todo, Priority
from sqlmodel import SQLModel


@pytest.fixture(scope="function")
def setup_test_env():
    """Set up test environment with SQLite database."""
    original_db_url = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///:memory:'

    yield

    if original_db_url is not None:
        os.environ['DATABASE_URL'] = original_db_url
    else:
        os.environ.pop('DATABASE_URL', None)


@pytest.fixture(scope="function")
async def db_engine():
    """Create a test database engine."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine):
    """Create a test database session."""
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest.fixture
async def client(db_session, setup_test_env):
    """Create async test client with database override."""
    # Override the database session in the app
    async def override_get_db():
        yield db_session

    app.dependency_overrides[async_session_maker] = lambda: override_get_db()

    async with ASGITransport(app=app) as transport:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    # Clear overrides after test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_todo_data():
    """Sample todo data for testing."""
    return {
        "title": "Test Todo",
        "description": "Test Description",
        "priority": "medium",
        "due_date": "2025-12-31T23:59:59",
        "completed": False
    }


@pytest.fixture
async def created_todo(db_session, sample_todo_data):
    """Create a todo in the database for testing."""
    from app.models.todo import Todo
    from datetime import datetime

    # Parse the date string
    due_date = datetime.fromisoformat(sample_todo_data["due_date"].replace("Z", "+00:00"))

    todo = Todo(
        title=sample_todo_data["title"],
        description=sample_todo_data["description"],
        priority=sample_todo_data["priority"],
        due_date=due_date,
        completed=sample_todo_data["completed"]
    )
    db_session.add(todo)
    await db_session.commit()
    await db_session.refresh(todo)
    return todo
