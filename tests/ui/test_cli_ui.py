from unittest.mock import patch

import pytest

from app.manager import TaskManager
from app.storages.in_memory import InMemoryTodoStorage
from app.ui.cli_ui import TodoCLIUI


@pytest.fixture
def cli_ui():
    storage = InMemoryTodoStorage()
    manager = TaskManager(repository=storage)
    return TodoCLIUI(task_manager=manager)


@patch(
    "builtins.input",
    side_effect=[
        'add --title "Test Task" --description "Test Description" --status no',
        "exit",
    ],
)
@patch("builtins.print")
def test_add_task(mock_print, mock_input, cli_ui):
    cli_ui.run()
    tasks = cli_ui.task_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == "Test Description"
    assert not tasks[0].is_done


@patch("builtins.input", side_effect=["list", "exit"])
@patch("builtins.print")
def test_list_tasks(mock_print, mock_input, cli_ui):
    cli_ui.task_manager.add_task("Task 1", "Description 1", False)
    cli_ui.run()
    mock_print.assert_any_call("\nTodo List:")
    mock_print.assert_any_call("[1] [ ] Task 1: Description 1")


@patch(
    "builtins.input",
    side_effect=[
        'update 1 --title "Updated Task" --description "Updated Description" --status yes',
        "exit",
    ],
)
@patch("builtins.print")
def test_update_task(mock_print, mock_input, cli_ui):
    cli_ui.task_manager.add_task("Task 1", "Description 1", False)
    cli_ui.run()
    tasks = cli_ui.task_manager.get_all_tasks()
    assert tasks[0].title == "Updated Task"
    assert tasks[0].description == "Updated Description"
    assert tasks[0].is_done
