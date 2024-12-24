import pytest
from fastapi.testclient import TestClient
from app.manager import TaskManager
from app.storages.in_memory import InMemoryTodoStorage
from app.ui.web_ui import TodoWebUI

@pytest.fixture
def client():
    storage = InMemoryTodoStorage()
    manager = TaskManager(repository=storage)
    web_ui = TodoWebUI(task_manager=manager)
    return TestClient(web_ui.app)

def test_add_todo(client):
    json_data = {
        "title": "Test Task",
        "description": "Test Description",
        "is_done": False
    }
    response = client.post("/todos", json=json_data)
    assert response.status_code == 201
    data = response.json()
    assert data["todo"]["title"] == "Test Task"
    assert data["todo"]["description"] == "Test Description"
    assert not data["todo"]["is_done"]

def test_list_todos(client):
    json_data = {
        "title": "Task 1",
        "description": "Description 1",
        "is_done": False
    }
    client.post("/todos", json=json_data)
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task 1" 