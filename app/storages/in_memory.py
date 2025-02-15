from app.models import Todo, User
from app.storages.base import NewTodo, NewUser, TodoStorage, UserStorage


class InMemoryUserStorage(UserStorage):
    def __init__(self):
        self.users: list[User] = []
        self.next_id: int = 1

    def add_user(self, new_user: NewUser) -> User:
        user = User(
            id=self.next_id,
            username=new_user.username,
            hashed_password=new_user.hashed_password,
            email=new_user.email,
            disabled=False,
        )
        self.users.append(user)
        self.next_id += 1
        return user

    def delete_user(self, user_id: int) -> None:
        self.users = [user for user in self.users if user.id != user_id]

    def get_user_by_id(self, user_id: int) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_user_by_username(self, username: str) -> User | None:
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_all_users(self) -> list[User]:
        return self.users

    def update_user(self, user: User) -> User | None:
        for i, u in enumerate(self.users):
            if u.id == user.id:
                self.users[i] = user
                return user
        return None


class InMemoryTodoStorage(TodoStorage):
    def __init__(self):
        self.todos: list[Todo] = []
        self.next_id: int = 1

    def add(self, new_todo: NewTodo) -> Todo:
        todo = Todo(
            id=self.next_id,
            user_id=new_todo.user_id,
            title=new_todo.title,
            description=new_todo.description,
            is_done=new_todo.is_done,
        )
        self.todos.append(todo)
        self.next_id += 1
        return todo

    def delete(self, todo_id: int) -> None:
        self.todos = [todo for todo in self.todos if todo.id != todo_id]

    def get_tasks_by_user_id(self, user_id: int) -> list[Todo]:
        return [todo for todo in self.todos if todo.user_id == user_id]

    def get_task_by_id(self, todo_id: int) -> Todo | None:
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_status(self, todo_id: int, is_done: bool) -> Todo | None:
        for todo in self.todos:
            if todo.id == todo_id:
                todo.is_done = is_done
                return todo
        return None

    def update(self, todo: Todo) -> Todo | None:
        for i, t in enumerate(self.todos):
            if t.id == todo.id:
                self.todos[i] = todo
                return todo
        return None


def get_in_memory_storage() -> tuple[InMemoryUserStorage, InMemoryTodoStorage]:
    return InMemoryUserStorage(), InMemoryTodoStorage()
