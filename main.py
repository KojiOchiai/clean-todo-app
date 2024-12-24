import argparse
from app.ui import TodoWebUI, TodoCLIUI
from app.storages import FileTodoStorage, InMemoryTodoStorage, SQLiteTodoStorage
from app.manager import TaskManager

def get_repository(storage_type: str):
    if storage_type == "file":
        file_path = "todo_data.json"
        return FileTodoStorage(file_path=file_path)
    elif storage_type == "memory":
        return InMemoryTodoStorage()
    elif storage_type == "sqlite":
        return SQLiteTodoStorage()
    else:
        raise ValueError("Invalid storage type. Use 'file', 'memory', or 'sqlite'.")

def get_ui(ui_type: str, task_manager: TaskManager):
    if ui_type == "web":
        return TodoWebUI(task_manager=task_manager)
    elif ui_type == "cli":
        return TodoCLIUI(task_manager=task_manager)
    else:
        raise ValueError("Invalid UI type. Use 'cli' or 'web'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Todo Application")
    parser.add_argument("--storage", choices=["file", "memory", "sqlite"], default="file", help="Type of storage to use")
    parser.add_argument("--ui", choices=["cli", "web"], default="cli", help="Type of UI to use")
    args = parser.parse_args()

    # Setup
    repository = get_repository(args.storage)
    task_manager = TaskManager(repository=repository)
    service = get_ui(args.ui, task_manager=task_manager)
    service.run()
