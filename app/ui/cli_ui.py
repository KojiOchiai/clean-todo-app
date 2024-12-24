from app.manager import TaskManager
from app.models import Todo
from app.ui.base import TodoInterface

class TodoCLIUI(TodoInterface):
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def run(self):
        def render(tasks: list[Todo]) -> str:
            return "\n".join(
                [
                    f"[{task.id}] [{'x' if task.is_done else ' '}] {task.title}: {task.description}"
                    for task in tasks
                ]
            )

        while True:
            print("\nCommands:")
            print("add - Add a new Todo")
            print("list - List all Todos")
            print("update - Update a Todo")
            print("delete - Delete a Todo")
            print("exit - Exit the application")

            command = input("Enter a command: ").strip().lower()

            if command == "add":
                title = input("Enter title: ").strip()
                description = input("Enter description: ").strip()
                is_done_input = input("Is it done? (yes/no, default is no): ").strip().lower()
                is_done = is_done_input == "yes" if is_done_input else False
                self.task_manager.add_task(title, description, is_done)
            elif command == "list":
                tasks = self.task_manager.get_all_tasks()
                print("\nTodo List:")
                print(render(tasks))
            elif command == "update":
                task_id = int(input("Enter task ID: ").strip())
                tasks = self.task_manager.get_all_tasks()
                for task in tasks:
                    if task.id == task_id:
                        new_title = input(f"Enter new title (current: {task.title}): ").strip() or task.title
                        new_description = input(f"Enter new description (current: {task.description}): ").strip() or task.description
                        new_status_input = input(f"Is it done? (yes/no, current: {'yes' if task.is_done else 'no'}): ").strip().lower()
                        new_status = new_status_input == "yes" if new_status_input else task.is_done
                        self.task_manager.update_task(task_id, new_title, new_description)
                        self.task_manager.set_task_status(task_id, new_status)
                        print(f"Todo with ID {task_id} updated.")
                        break
                else:
                    print(f"Todo with ID {task_id} not found.")
            elif command == "delete":
                task_id = int(input("Enter task ID to delete: ").strip())
                tasks = self.task_manager.get_all_tasks()
                if any(task.id == task_id for task in tasks):
                    self.task_manager.delete_task(task_id)
                    print(f"Todo with ID {task_id} deleted.")
                else:
                    print(f"Todo with ID {task_id} not found.")
            elif command == "exit":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid command. Please try again.") 