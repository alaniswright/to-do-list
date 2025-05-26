from fastapi.testclient import TestClient
from app.main import app
from app import models
from app.database import get_db, Base, engine
import pytest

# Setup a fresh test database (in-memory or dedicated test DB)
Base.metadata.create_all(bind=engine)
client = TestClient(app)

# Example test data
test_task = {
    "title": "Test Task",
    "published": True
}

def test_create_task():
    response = client.post("/tasks", json=test_task)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == test_task["title"]
    assert data["completed"] is False

def test_get_task():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_complete_task():
    # Create a task first
    post_resp = client.post("/tasks", json=test_task)
    task_id = post_resp.json()["id"]

    # Complete the task
    complete_resp = client.put(f"/tasks/complete/{task_id}")
    assert complete_resp.status_code == 200
    assert complete_resp.json()["completed"] is True

def test_uncomplete_task():
    # Create and complete a task
    post_resp = client.post("/tasks", json=test_task)
    task_id = post_resp.json()["id"]
    client.put(f"/tasks/complete/{task_id}")

    # Mark as not complete
    response = client.put(f"/tasks/undo-complete/{task_id}")
    assert response.status_code == 200
    assert response.json()["completed"] is False
    assert response.json()["completed_at"] is None

def test_delete_task():
    # Create a task
    post_resp = client.post("/tasks", json=test_task)
    task_id = post_resp.json()["id"]

    # Delete it
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 204

    # Confirm it's gone
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404