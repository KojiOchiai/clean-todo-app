from passlib.context import CryptContext

from app.models import Todo, User
from app.storages.base import NewTodo, NewUser, TodoStorage, UserStorage


class TaskManager:
    def __init__(self, storage: TodoStorage):
        self.storage = storage

    def add_task(self, title: str, description: str, is_done: bool = False) -> Todo:
        new_todo = NewTodo(title=title, description=description, is_done=is_done)
        todo = self.storage.add(new_todo)
        return todo

    def get_all_tasks(self) -> list[Todo]:
        return self.storage.get_all()

    def set_task_status(self, task_id: int, is_done: bool) -> None:
        task = self.storage.get_task(task_id)
        if task is None:
            raise ValueError("Task not found")
        self.storage.update_status(task_id, is_done)

    def delete_task(self, task_id: int) -> None:
        self.storage.delete(task_id)

    def update_task(
        self, task_id: int, title: str = None, description: str = None
    ) -> Todo:
        task = self.storage.get_task(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            self.storage.update(task)
            return task
        else:
            raise ValueError("Task not found")


class UserManager:
    def __init__(self, user_storage: UserStorage):
        self.storage = user_storage
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, username: str, email: str, password: str) -> User:
        if self.storage.get_user_by_email(email):
            raise ValueError("User already exists")
        hashed_password = self.hash_password(password)
        new_user = NewUser(
            username=username, email=email, hashed_password=hashed_password
        )
        return self.storage.add_user(new_user)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.storage.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        return user

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_user(self, user_id: int) -> User:
        return self.storage.get_user(user_id)

    def delete_user(self, user_id: int) -> None:
        self.storage.delete_user(user_id)

    def update_user(
        self,
        user_id: int,
        username: str = None,
        email: str = None,
        password: str = None,
    ) -> User:
        user = self.get_user(user_id)
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.hashed_password = self.hash_password(password)
            self.storage.update_user(user)
            return user
        else:
            raise ValueError("User not found")
