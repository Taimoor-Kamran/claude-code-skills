# SQLModel + FastAPI Integration Reference

## Table of Contents
1. [Project Setup](#project-setup)
2. [Engine & Lifespan](#engine--lifespan)
3. [Session Dependency](#session-dependency)
4. [Router Patterns](#router-patterns)
5. [Request & Response Models](#request--response-models)

---

## Project Setup

```bash
pip install fastapi sqlmodel uvicorn
```

Recommended structure:

```
app/
├── main.py          # FastAPI app + lifespan
├── database.py      # Engine + session dependency
├── models.py        # SQLModel table + data models
└── routers/
    └── heroes.py    # Route handlers
```

---

## Engine & Lifespan

```python
# database.py
from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

DATABASE_URL = "sqlite:///./database.db"
# For PostgreSQL: "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Run on startup
    yield
    # Teardown here if needed

app = FastAPI(lifespan=lifespan)
```

---

## Session Dependency

```python
# database.py
from typing import Generator
from sqlmodel import Session
from .database import engine

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

```python
# In routers
from fastapi import Depends
from sqlmodel import Session
from ..database import get_session

@router.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    ...
```

---

## Router Patterns

```python
# routers/heroes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from ..database import get_session
from ..models import Hero, HeroCreate, HeroRead, HeroUpdate

router = APIRouter(prefix="/heroes", tags=["heroes"])

@router.post("/", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get("/", response_model=list[HeroRead])
def read_heroes(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Hero).offset(offset).limit(limit)).all()

@router.get("/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.patch("/{hero_id}", response_model=HeroRead)
def update_hero(
    hero_id: int,
    hero_update: HeroUpdate,
    session: Session = Depends(get_session),
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero_update.model_dump(exclude_unset=True)
    hero.sqlmodel_update(hero_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@router.delete("/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

---

## Request & Response Models

```python
# models.py — full pattern with shared base
from typing import Optional
from sqlmodel import SQLModel, Field

class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass  # All base fields required

class HeroRead(HeroBase):
    id: int  # id exposed in responses

class HeroUpdate(SQLModel):
    name: Optional[str] = None       # All optional
    secret_name: Optional[str] = None
    age: Optional[int] = None
```

**Conversion:**

```python
# Create: Pydantic model → table model
db_hero = Hero.model_validate(hero_create)

# Partial update: apply only set fields
hero_data = hero_update.model_dump(exclude_unset=True)
hero.sqlmodel_update(hero_data)
```

**Register router in main.py:**

```python
from .routers import heroes
app.include_router(heroes.router)
```
