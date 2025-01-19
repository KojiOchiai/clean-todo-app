import shlex

from app.manager import TaskManager, UserManager
from app.models import Todo, User
from app.ui.base import TodoInterface


class TodoCLIUI(TodoInterface):
    def __init__(self, user_manager: UserManager, task_manager: TaskManager):
        self.user_manager = user_manager
        self.task_manager = task_manager

    def login(self, username: str, password: str) -> User:
        self.token = self.user_manager.login(username, password)
        return self.user_manager.get_user_by_token(self.token)

    def register(self, username: str, email: str, password: str) -> User:
        self.user_manager.create_user(username, email, password)
        return self.login(username, password)

    def get_user(self) -> User:
        return self.user_manager.get_user_by_token(self.token)

    def run(self):
        def render(task: Todo) -> str:
            return (
                f"[{task.id}] [{'x' if task.is_done else ' '}] "
                f"{task.title}: {task.description}"
            )

        def print_help():
            print("\nCommands:")
            print(
                (
                    "add --title <title> [--description <description>] "
                    "[--status <is_done>] - Add a new Todo"
                )
            )
            print("list - List all Todos")
            print(
                (
                    "update <id> [--title <new_title>] "
                    "[--description <new_description>] [--status <new_status>] "
                    "- Update a Todo"
                )
            )
            print("toggle <id> - Toggle the done status of a Todo")
            print("delete <id> - Delete a Todo")
            print("user_info - Display the current logged-in user information")
            print(
                (
                    "update_user --username <new_username> [--email <new_email>] "
                    "- Update user information"
                )
            )
            print("delete_user - Delete the current user account")
            print("help - Show this help message")
            print("exit - Exit the application")

        while True:
            print("Please login to continue, create a new account, or exit.")
            choice = input("Do you have an account? (yes/no/exit): ").strip().lower()
            if choice == "no":
                username = input("Choose a username: ").strip()
                email = input("Enter your email: ").strip()
                password = input("Choose a password: ").strip()
                try:
                    user = self.register(username, email, password)
                    print(f"Account created successfully! Welcome, {user.username}!")
                    break
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
            elif choice == "yes":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                try:
                    user = self.login(username, password)
                    print(f"Welcome, {user.username}!")
                    break
                except ValueError:
                    print("Invalid username or password. Please try again.")
            elif choice == "exit":
                print("Exiting... Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

        print_help()
        while True:
            command_input = input("\nEnter a command: ").strip()
            command_parts = shlex.split(command_input)
            command = command_parts[0]
            args = command_parts[1:]

            if command == "add":
                title = None
                description = ""
                is_done = False
                for i in range(0, len(args), 2):
                    if args[i] == "--title":
                        title = args[i + 1]
                    elif args[i] == "--description":
                        description = args[i + 1]
                    elif args[i] == "--status":
                        is_done = args[i + 1].lower() == "yes"
                if title is None:
                    print("Error: 'add' command requires a title.")
                    continue
                new_todo = self.task_manager.create_task(
                    self.get_user().id, title, description, is_done
                )
                print("Added Todo: " + render(new_todo))

            elif command == "list":
                tasks = self.task_manager.get_tasks_by_user_id(self.get_user().id)
                print("\nTodo List:")
                for task in tasks:
                    print(render(task))

            elif command == "update":
                if len(args) < 1:
                    print("Error: 'update' command requires at least an ID.")
                    continue
                task_id = int(args[0])
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
                updated_todo = self.task_manager.update_task(
                    self.get_user().id, task_id, new_title, new_description
                )
                if new_status is not None:
                    self.task_manager.set_task_status(
                        self.get_user().id, task_id, new_status
                    )
                    updated_todo = self.task_manager.update_task(
                        self.get_user().id, task_id
                    )
                print(render(updated_todo))

            elif command == "toggle":
                if len(args) < 1:
                    print("Error: 'toggle' command requires an ID.")
                    continue
                task_id = int(args[0])
                try:
                    task = self.task_manager.get_task_by_id(self.get_user().id, task_id)
                except ValueError:
                    print(f"Todo with ID {task_id} not found.")
                    continue
                task = self.task_manager.set_task_status(
                    self.get_user().id, task_id, not task.is_done
                )
                print(render(task))

            elif command == "delete":
                if len(args) < 1:
                    print("Error: 'delete' command requires an ID.")
                    continue
                task_id = int(args[0])
                tasks = self.task_manager.get_tasks_by_user_id(self.get_user().id)
                if any(task.id == task_id for task in tasks):
                    self.task_manager.delete_task(self.get_user().id, task_id)
                    print(f"Todo with ID {task_id} deleted.")
                else:
                    print(f"Todo with ID {task_id} not found.")

            elif command == "user_info":
                try:
                    user = self.get_user()
                    print(
                        (
                            f"User Information:\nUsername: {user.username}\nEmail: "
                            f"{user.email}"
                        )
                    )
                except ValueError as e:
                    print(f"Error: {e}")

            elif command == "update_user":
                new_username = None
                new_email = None
                for i in range(0, len(args), 2):
                    if args[i] == "--username":
                        new_username = args[i + 1]
                    elif args[i] == "--email":
                        new_email = args[i + 1]
                if new_username is None and new_email is None:
                    print(
                        (
                            "Error: 'update_user' command requires at least a new "
                            "username or email."
                        )
                    )
                    continue
                try:
                    updated_user = self.user_manager.update_user(
                        self.get_user().id, new_username, new_email
                    )
                    print(f"User updated successfully: {updated_user.username}")
                except ValueError as e:
                    print(f"Error: {e}")

            elif command == "delete_user":
                confirmation = (
                    input("Are you sure you want to delete your account? (yes/no): ")
                    .strip()
                    .lower()
                )
                if confirmation == "yes":
                    try:
                        self.user_manager.delete_user(self.get_user().id)
                        print("User account deleted successfully.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("User account deletion cancelled.")

            elif command == "help":
                print_help()

            elif command == "exit":
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid command. Please try again.")
