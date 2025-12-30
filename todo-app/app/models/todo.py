from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy import Column


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(255), index=True, nullable=False))
    description: str | None = Field(sa_column=Column(String, nullable=True))
    completed: bool = Field(default=False)
    priority: str = Field(sa_column=Column(String(10), nullable=False, default=Priority.MEDIUM.value))
    due_date: datetime | None = Field(sa_column=Column(DateTime, nullable=True))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=func.now()))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=func.now(), onupdate=func.now()))
