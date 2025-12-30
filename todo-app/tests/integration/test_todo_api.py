import pytest
from datetime import datetime
from httpx import AsyncClient
from app.models.todo import Priority


class TestTodoAPI:
    """Integration tests for Todo API endpoints."""

    @pytest.mark.asyncio
    async def test_create_todo(self, client):
        """Test creating a todo via API."""
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description",
            "priority": "high",
            "due_date": "2025-12-31T23:59:59"
        }

        response = await client.post("/api/v1/todos/", json=todo_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test Description"
        assert data["priority"] == "high"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_todo_minimal_data(self, client):
        """Test creating a todo with minimal data."""
        todo_data = {
            "title": "Minimal Todo"
        }

        response = await client.post("/api/v1/todos/", json=todo_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Todo"
        assert data["priority"] == "medium"  # Default priority
        assert data["completed"] is False

    @pytest.mark.asyncio
    async def test_create_todo_validation_error(self, client):
        """Test creating a todo with invalid data."""
        todo_data = {
            "title": ""  # Empty title should fail validation
        }

        response = await client.post("/api/v1/todos/", json=todo_data)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_get_todo(self, client):
        """Test getting a todo by ID via API."""
        # First create a todo
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description"
        }
        create_response = await client.post("/api/v1/todos/", json=todo_data)
        created_data = create_response.json()
        todo_id = created_data["id"]

        # Get the todo
        response = await client.get(f"/api/v1/todos/{todo_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test Todo"

    @pytest.mark.asyncio
    async def test_get_todo_not_found(self, client):
        """Test getting a non-existent todo."""
        response = await client.get("/api/v1/todos/999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_list_todos(self, client):
        """Test listing todos via API."""
        # Create multiple todos
        todo_data1 = {"title": "Todo 1", "priority": "low"}
        todo_data2 = {"title": "Todo 2", "priority": "high"}

        await client.post("/api/v1/todos/", json=todo_data1)
        await client.post("/api/v1/todos/", json=todo_data2)

        response = await client.get("/api/v1/todos/")

        assert response.status_code == 200
        data = response.json()
        assert "todos" in data
        assert "total" in data
        assert data["total"] >= 2
        assert len(data["todos"]) >= 2

    @pytest.mark.asyncio
    async def test_list_todos_with_filters(self, client):
        """Test listing todos with various filters."""
        # Create todos with different attributes
        await client.post("/api/v1/todos/", json={
            "title": "High Priority Todo",
            "priority": "high",
            "completed": False
        })
        await client.post("/api/v1/todos/", json={
            "title": "Completed Todo",
            "priority": "medium",
            "completed": True
        })
        await client.post("/api/v1/todos/", json={
            "title": "Low Priority Todo",
            "priority": "low",
            "completed": False,
            "due_date": "2025-01-15T10:00:00"
        })

        # Test priority filter
        response = await client.get("/api/v1/todos/?priority=high")
        data = response.json()
        assert response.status_code == 200
        high_priority_todos = [t for t in data["todos"] if t["priority"] == "high"]
        assert len(high_priority_todos) >= 1

        # Test completion filter
        response = await client.get("/api/v1/todos/?completed=true")
        data = response.json()
        assert response.status_code == 200
        completed_todos = [t for t in data["todos"] if t["completed"] is True]
        assert len(completed_todos) >= 1

        # Test search filter
        response = await client.get("/api/v1/todos/?search=High Priority")
        data = response.json()
        assert response.status_code == 200
        search_results = [t for t in data["todos"] if "High Priority" in t["title"]]
        assert len(search_results) >= 1

        # Test date filter
        response = await client.get("/api/v1/todos/?date_from=2025-01-01T00:00:00")
        data = response.json()
        assert response.status_code == 200
        # Should include todos with due dates after Jan 1, 2025

    @pytest.mark.asyncio
    async def test_update_todo(self, client):
        """Test updating a todo via API."""
        # Create a todo first
        todo_data = {
            "title": "Original Todo",
            "description": "Original Description",
            "priority": "low"
        }
        create_response = await client.post("/api/v1/todos/", json=todo_data)
        created_data = create_response.json()
        todo_id = created_data["id"]

        # Update the todo
        update_data = {
            "title": "Updated Todo",
            "description": "Updated Description",
            "priority": "high",
            "completed": True
        }
        response = await client.patch(f"/api/v1/todos/{todo_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Updated Todo"
        assert data["description"] == "Updated Description"
        assert data["priority"] == "high"
        assert data["completed"] is True

    @pytest.mark.asyncio
    async def test_update_todo_partial(self, client):
        """Test partially updating a todo."""
        # Create a todo first
        todo_data = {
            "title": "Original Todo",
            "description": "Original Description"
        }
        create_response = await client.post("/api/v1/todos/", json=todo_data)
        created_data = create_response.json()
        todo_id = created_data["id"]

        # Partially update the todo
        update_data = {
            "title": "Updated Title Only"
        }
        response = await client.patch(f"/api/v1/todos/{todo_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Updated Title Only"
        assert data["description"] == "Original Description"  # Unchanged

    @pytest.mark.asyncio
    async def test_update_todo_not_found(self, client):
        """Test updating a non-existent todo."""
        update_data = {"title": "Updated Todo"}
        response = await client.patch("/api/v1/todos/999", json=update_data)

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_delete_todo(self, client):
        """Test deleting a todo via API."""
        # Create a todo first
        todo_data = {"title": "Todo to Delete"}
        create_response = await client.post("/api/v1/todos/", json=todo_data)
        created_data = create_response.json()
        todo_id = created_data["id"]

        # Verify todo exists
        get_response = await client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 200

        # Delete the todo
        response = await client.delete(f"/api/v1/todos/{todo_id}")

        assert response.status_code == 204  # No content

        # Verify todo no longer exists
        get_response = await client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_todo_not_found(self, client):
        """Test deleting a non-existent todo."""
        response = await client.delete("/api/v1/todos/999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_toggle_todo_complete(self, client):
        """Test toggling a todo's completion status."""
        # Create a todo first
        todo_data = {
            "title": "Toggle Todo",
            "completed": False
        }
        create_response = await client.post("/api/v1/todos/", json=todo_data)
        created_data = create_response.json()
        todo_id = created_data["id"]

        # Toggle completion
        response = await client.post(f"/api/v1/todos/{todo_id}/toggle")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["completed"] is True  # Should be toggled to True

        # Toggle again
        response = await client.post(f"/api/v1/todos/{todo_id}/toggle")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["completed"] is False  # Should be toggled back to False

    @pytest.mark.asyncio
    async def test_toggle_todo_not_found(self, client):
        """Test toggling completion for a non-existent todo."""
        response = await client.post("/api/v1/todos/999/toggle")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_list_todos_pagination(self, client):
        """Test pagination of todos via API."""
        # Create 5 todos
        for i in range(5):
            await client.post("/api/v1/todos/", json={"title": f"Todo {i+1}"})

        # Get first 2 todos
        response = await client.get("/api/v1/todos/?skip=0&limit=2")
        data = response.json()

        assert response.status_code == 200
        assert len(data["todos"]) == 2
        assert data["total"] >= 5

        # Get next 2 todos
        response = await client.get("/api/v1/todos/?skip=2&limit=2")
        data = response.json()

        assert response.status_code == 200
        assert len(data["todos"]) == 2

    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Test health check endpoint."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"