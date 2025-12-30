"""Database configuration."""
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

def get_engine():
    """Get database engine, can be overridden for testing."""
    import os
    from urllib.parse import urlparse, urlunparse, unquote

    # Use a test database if DATABASE_URL_OVERRIDE environment variable is set
    db_url = os.getenv("DATABASE_URL_OVERRIDE", settings.DATABASE_URL)

    # Automatically adjust PostgreSQL URLs to use asyncpg driver if not already specified
    if db_url.startswith("postgresql://") and not db_url.startswith("postgresql+asyncpg://"):
        # Parse the URL to properly handle the path (database name) and remove query parameters
        parsed = urlparse(db_url)
        # Unquote the path to handle URL encoding (e.g., %20 for space)
        unquoted_path = unquote(parsed.path)
        # Create a new URL with asyncpg scheme but without query parameters
        new_parsed = parsed._replace(scheme='postgresql+asyncpg', query='', path=unquoted_path)
        db_url = urlunparse(new_parsed)

    return create_async_engine(
        db_url,
        echo=settings.DEBUG,
    )


# Create the engine instance
engine = get_engine()

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
