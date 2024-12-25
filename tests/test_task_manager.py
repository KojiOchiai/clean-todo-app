import pytest

from app.manager import TaskManager
from app.storages.in_memory import InMemoryTodoStorage


@pytest.fixture
def manager():
    storage = InMemoryTodoStorage()
    return TaskManager(repository=storage)


def test_add_task(manager):
    new_todo = manager.add_task("Test Task", "This is a test task", False)
    assert new_todo.title == "Test Task"
    assert new_todo.description == "This is a test task"
    assert not new_todo.is_done


def test_get_all_tasks(manager):
    manager.add_task("Task 1", "Description 1", False)
    manager.add_task("Task 2", "Description 2", True)
    tasks = manager.get_all_tasks()
    assert len(tasks) == 2


def test_update_task(manager):
    new_todo = manager.add_task("Test Task", "This is a test task", False)
    updated_todo = manager.update_task(
        new_todo.id, "Updated Task", "Updated description"
    )
    assert updated_todo.title == "Updated Task"
    assert updated_todo.description == "Updated description"


def test_update_task_not_found(manager):
    with pytest.raises(ValueError, match="Task not found"):
        manager.update_task(999, "Non-existent Task", "No description")


def test_toggle_task_status(manager):
    new_todo = manager.add_task("Test Task", "This is a test task", False)
    manager.set_task_status(new_todo.id, True)
    task = manager.repository.get_task(new_todo.id)
    assert task.is_done


def test_toggle_task_status_not_found(manager):
    with pytest.raises(ValueError, match="Task not found"):
        manager.set_task_status(999, True)


def test_delete_task(manager):
    new_todo = manager.add_task("Test Task", "This is a test task", False)
    manager.delete_task(new_todo.id)
    tasks = manager.get_all_tasks()
    assert len(tasks) == 0


def test_delete_task_not_found(manager):
    # Ensure no exception is raised for deleting a non-existent task
    manager.delete_task(999)
    tasks = manager.get_all_tasks()
    assert len(tasks) == 0
