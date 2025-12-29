"""Tests for items API."""
import pytest


@pytest.mark.asyncio
async def test_create_item(client):
    """Test creating an item."""
    response = await client.post(
        "/api/v1/items/",
        json={"name": "Test Item", "price": 10.99},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.99
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items(client):
    """Test listing items."""
    response = await client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
