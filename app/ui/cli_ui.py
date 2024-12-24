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
            print("add <title> [description] [is_done] - Add a new Todo")
            print("list - List all Todos")
            print("update <id> [--title new_title] [--description new_description] [--status new_status] - Update a Todo")
            print("toggle <id> - Toggle the done status of a Todo")
            print("delete <id> - Delete a Todo")
            print("exit - Exit the application")

            command_input = input("Enter a command: ").strip().lower()
            command_parts = command_input.split()
            command = command_parts[0]
            args = command_parts[1:]

            if command == "add":
                if len(args) < 1:
                    print("Error: 'add' command requires at least a title.")
                    continue
                title = args[0]
                description = args[1] if len(args) > 1 else ""
                is_done = args[2].lower() == "yes" if len(args) > 2 else False
                new_todo = self.task_manager.add_task(title, description, is_done)
                print(f"Added Todo: [{new_todo.id}] {new_todo.title}: {new_todo.description} (Done: {new_todo.is_done})")
            elif command == "list":
                tasks = self.task_manager.get_all_tasks()
                print("\nTodo List:")
                print(render(tasks))
            elif command == "update":
                if len(args) < 1:
                    print("Error: 'update' command requires at least an ID.")
                    continue
                task_id = int(args[0])
                tasks = self.task_manager.get_all_tasks()
                new_title = None
                new_description = None
                new_status = None
                for i in range(1, len(args), 2):
                    if args[i] == "--title":
                        new_title = args[i + 1]
                    elif args[i] == "--description":
                        new_description = args[i + 1]
                    elif args[i] == "--status":
                        new_status = args[i + 1].lower() == "yes"
                for task in tasks:
                    if task.id == task_id:
                        updated_task = self.task_manager.update_task(task_id, new_title, new_description)
                        if new_status is not None:
                            self.task_manager.set_task_status(task_id, new_status)
                            updated_task = self.task_manager.update_task(task_id)  # 状態を再取得
                        print(f"Updated Todo: [{updated_task.id}] {updated_task.title}: {updated_task.description} (Done: {updated_task.is_done})")
                        break
                else:
                    print(f"Todo with ID {task_id} not found.")
            elif command == "toggle":
                if len(args) < 1:
                    print("Error: 'toggle' command requires an ID.")
                    continue
                task_id = int(args[0])
                tasks = self.task_manager.get_all_tasks()
                for task in tasks:
                    if task.id == task_id:
                        new_status = not task.is_done
                        self.task_manager.set_task_status(task_id, new_status)
                        print(f"Todo with ID {task_id} status toggled to {'done' if new_status else 'not done'}.")
                        break
                else:
                    print(f"Todo with ID {task_id} not found.")
            elif command == "delete":
                if len(args) < 1:
                    print("Error: 'delete' command requires an ID.")
                    continue
                task_id = int(args[0])
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