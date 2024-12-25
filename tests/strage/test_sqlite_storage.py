import pytest

from app.storages.base import NewTodo
from app.storages.sqlite_storage import SQLiteTodoStorage


@pytest.fixture
def storage():
    # Use an in-memory SQLite database for testing
    storage = SQLiteTodoStorage(db_url="sqlite:///:memory:")
    yield storage
    # No need to clean up as the in-memory database is discarded after the session


def test_add_and_get_task(storage):
    new_todo = NewTodo(
        title="Test Task", description="This is a test task", is_done=False
    )
    todo = storage.add(new_todo)
    retrieved_todo = storage.get_task(todo.id)
    assert retrieved_todo.title == "Test Task"
    assert retrieved_todo.description == "This is a test task"
    assert not retrieved_todo.is_done


def test_update_task(storage):
    new_todo = NewTodo(
        title="Test Task", description="This is a test task", is_done=False
    )
    todo = storage.add(new_todo)
    todo.title = "Updated Task"
    todo.description = "Updated description"
    storage.update(todo)
    updated_todo = storage.get_task(todo.id)
    assert updated_todo.title == "Updated Task"
    assert updated_todo.description == "Updated description"


def test_delete_task(storage):
    new_todo = NewTodo(
        title="Test Task", description="This is a test task", is_done=False
    )
    todo = storage.add(new_todo)
    storage.delete(todo.id)
    assert storage.get_task(todo.id) is None


def test_get_task_not_found(storage):
    assert storage.get_task(999) is None


def test_update_status(storage):
    new_todo = NewTodo(
        title="Test Task", description="This is a test task", is_done=False
    )
    todo = storage.add(new_todo)
    storage.update_status(todo.id, True)
    updated_todo = storage.get_task(todo.id)
    assert updated_todo.is_done


def test_update_status_not_found(storage):
    # Ensure no exception is raised for updating status of a non-existent task
    storage.update_status(999, True)
    assert storage.get_task(999) is None
