import argparse

from app.manager import TaskManager, UserManager
from app.storages import (
    FileTodoStorage,
    FileUserStorage,
    InMemoryTodoStorage,
    InMemoryUserStorage,
    SQLiteTodoStorage,
)
from app.ui import TodoCLIUI, TodoWebUI


def get_storage(storage_type: str):
    if storage_type == "file":
        todo_file_path = "todo_data.json"
        user_file_path = "user_data.json"
        return (
            FileUserStorage(file_path=user_file_path),
            FileTodoStorage(file_path=todo_file_path),
        )
    elif storage_type == "memory":
        return InMemoryUserStorage(), InMemoryTodoStorage()
    elif storage_type == "sqlite":
        return SQLiteTodoStorage()
    else:
        raise ValueError("Invalid storage type. Use 'file', 'memory', or 'sqlite'.")


def get_ui(ui_type: str, user_manager: UserManager, task_manager: TaskManager):
    if ui_type == "web":
        return TodoWebUI(user_manager=user_manager, task_manager=task_manager)
    elif ui_type == "cli":
        return TodoCLIUI(user_manager=user_manager, task_manager=task_manager)
    else:
        raise ValueError("Invalid UI type. Use 'cli' or 'web'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Todo Application")
    parser.add_argument(
        "--storage",
        choices=["file", "memory", "sqlite"],
        default="file",
        help="Type of storage to use",
    )
    parser.add_argument(
        "--ui", choices=["cli", "web"], default="cli", help="Type of UI to use"
    )
    args = parser.parse_args()

    # Setup
    user_storage, todo_storage = get_storage(args.storage)
    user_manager = UserManager(storage=user_storage, secret_key="secret")
    task_manager = TaskManager(storage=todo_storage)
    service = get_ui(args.ui, user_manager=user_manager, task_manager=task_manager)
    service.run()
