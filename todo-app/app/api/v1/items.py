"""Items API endpoints."""
from fastapi import APIRouter, HTTPException

from app.schemas.item import Item, ItemCreate

router = APIRouter()

# In-memory storage for demo (replace with database in production)
items_db: dict[int, Item] = {}
item_counter = 0


@router.get("/", response_model=list[Item])
async def list_items():
    """List all items."""
    return list(items_db.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    global item_counter
    item_counter += 1
    db_item = Item(id=item_counter, **item.model_dump())
    items_db[item_counter] = db_item
    return db_item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
