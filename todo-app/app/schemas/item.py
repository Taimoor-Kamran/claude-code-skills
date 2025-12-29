"""Item schemas."""
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base item schema."""
    name: str
    description: str | None = None
    price: float


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    pass


class Item(ItemBase):
    """Schema for item response."""
    id: int

    model_config = {"from_attributes": True}
