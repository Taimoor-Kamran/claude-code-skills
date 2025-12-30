"""Application configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields in .env
    )

    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    DATABASE_API_KEY: str = ""  # Optional API key for database
    OPENAI_API_KEY: str = ""  # Optional OpenAI API key


settings = Settings()
