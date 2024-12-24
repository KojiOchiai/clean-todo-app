from app.ui import TodoWebUI, TodoCLIUI
from app.storages import FileTodoStorage, InMemoryTodoStorage
from app.manager import TaskManager

def get_repository():
    while True:
        choice = input("Choose repository (file/memory): ").strip().lower()
        if choice == "file":
            file_path = "todo_data.json"
            return FileTodoStorage(file_path=file_path)
        elif choice == "memory":
            return InMemoryTodoStorage()
        else:
            print("Invalid choice. Please enter 'file' or 'memory'.")

def get_ui(task_manager: TaskManager):
    while True:
        choice = input("Choose UI (cli/web): ").strip().lower()
        if choice == "web":
            return TodoWebUI(task_manager=task_manager)
        elif choice == "cli":
            return TodoCLIUI(task_manager=task_manager)
        else:
            print("Invalid choice. Please enter 'cli' or 'web'.")

if __name__ == "__main__":
    # Setup
    repository = get_repository()
    task_manager = TaskManager(repository=repository)
    service = get_ui(task_manager=task_manager)
    service.run()
