# SQLModel CRUD Reference

## Table of Contents
1. [Create](#create)
2. [Read](#read)
3. [Update](#update)
4. [Delete](#delete)
5. [Filtering & Ordering](#filtering--ordering)
6. [Pagination](#pagination)

---

## Create

```python
from sqlmodel import Session

with Session(engine) as session:
    # Single record
    hero = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    session.add(hero)
    session.commit()
    session.refresh(hero)  # Reload from DB (gets generated id, defaults, etc.)
    print(hero.id)         # Now has the DB-assigned id

    # Multiple records
    heroes = [
        Hero(name="Deadpond", secret_name="Dive Wilson"),
        Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48),
    ]
    for h in heroes:
        session.add(h)
    session.commit()
```

---

## Read

```python
from sqlmodel import Session, select

with Session(engine) as session:
    # By primary key (returns None if not found)
    hero = session.get(Hero, hero_id)

    # All records
    statement = select(Hero)
    heroes = session.exec(statement).all()

    # First match
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    hero = session.exec(statement).first()

    # One or raise (raises NoResultFound if not found)
    hero = session.exec(statement).one()
```

---

## Update

```python
with Session(engine) as session:
    # Fetch, modify, commit
    hero = session.get(Hero, hero_id)
    if not hero:
        raise ValueError(f"Hero {hero_id} not found")

    hero.age = 16
    session.add(hero)
    session.commit()
    session.refresh(hero)

    # Partial update from dict (e.g., from HeroUpdate Pydantic model)
    hero_data = hero_update.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)
    session.add(hero)
    session.commit()
    session.refresh(hero)
```

---

## Delete

```python
with Session(engine) as session:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise ValueError(f"Hero {hero_id} not found")

    session.delete(hero)
    session.commit()
    # hero is now detached — don't use it after commit
```

---

## Filtering & Ordering

```python
from sqlmodel import select, col

with Session(engine) as session:
    # WHERE conditions
    statement = select(Hero).where(Hero.age >= 18)
    statement = select(Hero).where(Hero.age >= 18, Hero.name != "Deadpond")  # AND

    # OR condition
    from sqlalchemy import or_
    statement = select(Hero).where(or_(Hero.age < 18, Hero.age > 65))

    # LIKE / contains
    statement = select(Hero).where(col(Hero.name).contains("man"))
    statement = select(Hero).where(col(Hero.name).startswith("Spider"))

    # ORDER BY
    statement = select(Hero).order_by(Hero.age)
    statement = select(Hero).order_by(col(Hero.age).desc())

    # LIMIT
    statement = select(Hero).limit(10)

    # OFFSET + LIMIT (pagination)
    statement = select(Hero).offset(20).limit(10)

    heroes = session.exec(statement).all()
```

---

## Pagination

```python
def get_heroes(
    session: Session,
    offset: int = 0,
    limit: int = 100,
) -> list[Hero]:
    return session.exec(
        select(Hero).offset(offset).limit(limit)
    ).all()

# Count total for pagination metadata
from sqlalchemy import func
total = session.exec(select(func.count()).select_from(Hero)).one()
```

**FastAPI pagination endpoint:**

```python
@router.get("/heroes/", response_model=list[HeroRead])
def read_heroes(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
```
