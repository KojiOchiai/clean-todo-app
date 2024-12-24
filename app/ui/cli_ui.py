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
            print("\nOptions:")
            print("1. Add Todo")
            print("2. List Todos")
            print("3. Update Todo Status")
            print("4. Delete Todo")
            print("5. Exit")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                title = input("Enter title: ").strip()
                description = input("Enter description: ").strip()
                is_done_input = input("Is it done? (yes/no, default is no): ").strip().lower()
                is_done = is_done_input == "yes" if is_done_input else False
                self.task_manager.add_task(title, description, is_done)
            elif choice == "2":
                tasks = self.task_manager.get_all_tasks()
                print("\nTodo List:")
                print(render(tasks))
            elif choice == "3":
                task_id = int(input("Enter task ID: ").strip())
                is_done = input("Is it done? (yes/no): ").strip().lower() == "yes"
                self.task_manager.set_task_status(task_id, is_done)
            elif choice == "4":
                print("Exiting... Goodbye!")
                break
            elif choice == "5":
                task_id = int(input("Enter task ID to delete: ").strip())
                self.task_manager.delete_task(task_id)
                print(f"Todo with ID {task_id} deleted.")
            else:
                print("Invalid option. Please try again.") 