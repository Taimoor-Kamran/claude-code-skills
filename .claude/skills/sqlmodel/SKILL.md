---
name: sqlmodel
description: SQLModel Python ORM development assistance using official Context7 documentation. Use when building database models, sessions, CRUD operations, relationships, or FastAPI + SQLModel integration. Triggers on SQLModel model definition, query patterns, session management, table relationships, migration with Alembic, or any SQLModel-related development task.
---

# SQLModel

SQLModel is a Python library for interacting with SQL databases using Python objects. It combines SQLAlchemy and Pydantic, making it ideal for FastAPI applications.

## Fetch Official Docs

Always fetch official SQLModel docs via Context7 before writing code:

```bash
# Fetch by topic (recommended)
bash scripts/fetch-sqlmodel-docs.sh --topic <topic>

# Examples:
bash scripts/fetch-sqlmodel-docs.sh --topic "create models"
bash scripts/fetch-sqlmodel-docs.sh --topic "session query"
bash scripts/fetch-sqlmodel-docs.sh --topic "relationships"
bash scripts/fetch-sqlmodel-docs.sh --topic "FastAPI integration"
bash scripts/fetch-sqlmodel-docs.sh --topic "select where"
```

SQLModel Context7 ID: `/fastapi/sqlmodel`

## Workflow

1. **Fetch docs** for the relevant topic (`bash scripts/fetch-sqlmodel-docs.sh --topic <topic>`)
2. **Implement** using fetched patterns
3. **For complex topics**, see reference files below

## Core Patterns

### Model Definition

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
```

- `table=True` → database table model
- No `table=True` → Pydantic-only data model (for request/response schemas)

### Session & Engine

```python
from sqlmodel import create_engine, Session, SQLModel

engine = create_engine("sqlite:///database.db")

def create_db():
    SQLModel.metadata.create_all(engine)

# Use session as context manager
with Session(engine) as session:
    session.add(hero)
    session.commit()
    session.refresh(hero)
```

### CRUD Quick Reference

```python
from sqlmodel import Session, select

# Create
hero = Hero(name="Spider-Boy", secret_name="Pedro")
session.add(hero)
session.commit()

# Read one
hero = session.get(Hero, hero_id)

# Read many
statement = select(Hero).where(Hero.name == "Spider-Boy")
heroes = session.exec(statement).all()

# Update
hero.age = 16
session.add(hero)
session.commit()

# Delete
session.delete(hero)
session.commit()
```

## Reference Files

Load these only when needed:

- **[references/models.md](references/models.md)** - Model fields, validators, optional vs required, inheritance, table vs data models
- **[references/relationships.md](references/relationships.md)** - One-to-many, many-to-many, back_populates, Relationship()
- **[references/crud.md](references/crud.md)** - Full CRUD patterns, filtering, ordering, pagination, exec() vs all()
- **[references/fastapi-integration.md](references/fastapi-integration.md)** - Lifespan events, session dependency, router patterns, request/response models
