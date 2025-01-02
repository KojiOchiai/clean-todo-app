import argparse
import os

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.manager import TaskManager, UserManager
from app.storages import get_file_storage, get_in_memory_storage, get_sqlite_storage
from app.storages.base import TodoStorage, UserStorage
from app.ui import TodoCLIUI, TodoWebUI

load_dotenv()


def get_storage(storage_type: str) -> tuple[UserStorage, TodoStorage]:
    if storage_type == "file":
        return get_file_storage("data")
    elif storage_type == "memory":
        return get_in_memory_storage()
    elif storage_type == "sqlite":
        return get_sqlite_storage("sqlite:///todos.db")
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
    user_manager = UserManager(storage=user_storage, secret_key=os.getenv("SECRET_KEY"))
    task_manager = TaskManager(storage=todo_storage)
    service = get_ui(args.ui, user_manager=user_manager, task_manager=task_manager)
    service.run()
