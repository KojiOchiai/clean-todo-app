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
            print("1. Add Todo (or type 'add')")
            print("2. List Todos (or type 'list')")
            print("3. Update Todo Status (or type 'update')")
            print("4. Delete Todo (or type 'delete')")
            print("5. Exit (or type 'exit')")

            choice = input("Choose an option: ").strip().lower()
            if choice in ["1", "add"]:
                title = input("Enter title: ").strip()
                description = input("Enter description: ").strip()
                is_done_input = input("Is it done? (yes/no, default is no): ").strip().lower()
                is_done = is_done_input == "yes" if is_done_input else False
                self.task_manager.add_task(title, description, is_done)
            elif choice in ["2", "list"]:
                tasks = self.task_manager.get_all_tasks()
                print("\nTodo List:")
                print(render(tasks))
            elif choice in ["3", "update"]:
                task_id = int(input("Enter task ID: ").strip())
                tasks = self.task_manager.get_all_tasks()
                for task in tasks:
                    if task.id == task_id:
                        new_status = not task.is_done
                        self.task_manager.set_task_status(task_id, new_status)
                        print(f"Todo with ID {task_id} status toggled to {'done' if new_status else 'not done'}.")
                        break
                else:
                    print(f"Todo with ID {task_id} not found.")
            elif choice in ["4", "delete"]:
                task_id = int(input("Enter task ID to delete: ").strip())
                self.task_manager.delete_task(task_id)
                print(f"Todo with ID {task_id} deleted.")
            elif choice in ["5", "exit"]:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid option. Please try again.") 