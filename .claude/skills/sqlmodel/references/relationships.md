# SQLModel Relationships Reference

## Table of Contents
1. [One-to-Many](#one-to-many)
2. [Many-to-Many](#many-to-many)
3. [Optional Relationships](#optional-relationships)
4. [Accessing Related Data](#accessing-related-data)

---

## One-to-Many

```python
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: Optional[str] = None

    # Back reference to list of heroes
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    # Reference to single team
    team: Optional[Team] = Relationship(back_populates="heroes")
```

**Rules:**
- Always define `foreign_key` on the "many" side (Hero)
- Use `back_populates` on both sides with matching attribute names
- Wrap the "one" side type in `List[...]`; the "many" side in `Optional[...]`

---

## Many-to-Many

```python
# Link table (junction table)
class HeroTeamLink(SQLModel, table=True):
    hero_id: Optional[int] = Field(
        default=None, foreign_key="hero.id", primary_key=True
    )
    team_id: Optional[int] = Field(
        default=None, foreign_key="team.id", primary_key=True
    )

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    teams: List[Team] = Relationship(
        back_populates="heroes", link_model=HeroTeamLink
    )

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    heroes: List[Hero] = Relationship(
        back_populates="teams", link_model=HeroTeamLink
    )
```

---

## Optional Relationships

```python
# One-to-one (optional on both sides)
class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    street: str
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id")
    hero: Optional["Hero"] = Relationship(back_populates="address")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: Optional[Address] = Relationship(back_populates="hero")
```

---

## Accessing Related Data

```python
from sqlmodel import Session, select

with Session(engine) as session:
    # Get hero with related team (lazy loaded)
    hero = session.get(Hero, 1)
    # Access within session — triggers lazy load
    print(hero.team.name)

    # Eager loading via selectinload
    from sqlalchemy.orm import selectinload
    statement = select(Hero).options(selectinload(Hero.team))
    heroes = session.exec(statement).all()
    # Now hero.team is available outside session

# Adding a relationship
with Session(engine) as session:
    team = session.get(Team, 1)
    new_hero = Hero(name="Spider-Boy", secret_name="Pedro", team=team)
    session.add(new_hero)
    session.commit()
```

**Note:** Lazy loading only works within an active session. Use `selectinload` or `joinedload` for access outside the session context.
