# SQLModel Models Reference

## Table of Contents
1. [Table vs Data Models](#table-vs-data-models)
2. [Field Types & Options](#field-types--options)
3. [Validators](#validators)
4. [Model Inheritance](#model-inheritance)

---

## Table vs Data Models

```python
from sqlmodel import SQLModel, Field
from typing import Optional

# TABLE MODEL — maps to a DB table
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

# DATA MODEL — Pydantic only (no DB table), for request/response schemas
class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

class HeroRead(SQLModel):
    id: int
    name: str
    age: Optional[int] = None

class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
```

**Rule:** Use `table=True` only for database tables. Create separate data models for API request/response to avoid exposing all fields.

---

## Field Types & Options

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Item(SQLModel, table=True):
    # Primary key (auto-increment)
    id: Optional[int] = Field(default=None, primary_key=True)

    # Required string with DB index
    name: str = Field(index=True)

    # Optional with default
    description: Optional[str] = Field(default=None, max_length=300)

    # Unique constraint
    code: str = Field(unique=True)

    # Foreign key
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    # Custom column name
    full_name: str = Field(sa_column_kwargs={"name": "fullname"})

    # Timestamp with default factory
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Nullable field
    price: Optional[float] = None
```

**Field() key parameters:**
| Parameter | Purpose |
|-----------|---------|
| `default` | Default value |
| `default_factory` | Callable for default |
| `primary_key=True` | Primary key |
| `index=True` | DB index |
| `unique=True` | Unique constraint |
| `foreign_key="table.col"` | Foreign key reference |
| `nullable=False` | Override nullability |
| `max_length=N` | String max length (Pydantic + DB) |

---

## Validators

```python
from sqlmodel import SQLModel, Field
from pydantic import validator, field_validator

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None

    # Pydantic v2 style
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v.strip()

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("age must be non-negative")
        return v
```

---

## Model Inheritance

```python
# Base with shared fields (no table)
class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

# Table model inherits from base
class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# API models inherit from same base — consistent fields
class HeroCreate(HeroBase):
    pass  # Same fields as base, no id

class HeroRead(HeroBase):
    id: int  # Add id for responses

class HeroUpdate(SQLModel):
    # All optional for partial updates
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
```

This pattern avoids field duplication and keeps API/DB models in sync.
