import pytest
import os
from app.models import Todo
from app.storages.file_storage import FileTodoStorage

@pytest.fixture
def storage():
    file_path = "test_todo_data.json"
    storage = FileTodoStorage(file_path=file_path)
    yield storage
    if os.path.exists(file_path):
        os.remove(file_path)

def test_add_and_get_task(storage):
    todo = Todo(
        id=storage.get_next_id(),
        title="Test Task",
        description="This is a test task",
        is_done=False
    )
    storage.add(todo)
    retrieved_todo = storage.get_task(todo.id)
    assert retrieved_todo.title == "Test Task"
    assert retrieved_todo.description == "This is a test task"
    assert not retrieved_todo.is_done

def test_update_task(storage):
    todo = Todo(
        id=storage.get_next_id(),
        title="Test Task",
        description="This is a test task",
        is_done=False
    )
    storage.add(todo)
    todo.title = "Updated Task"
    todo.description = "Updated description"
    storage.update(todo)
    updated_todo = storage.get_task(todo.id)
    assert updated_todo.title == "Updated Task"
    assert updated_todo.description == "Updated description"

def test_delete_task(storage):
    todo = Todo(
        id=storage.get_next_id(),
        title="Test Task",
        description="This is a test task",
        is_done=False
    )
    storage.add(todo)
    storage.delete(todo.id)
    assert storage.get_task(todo.id) is None 