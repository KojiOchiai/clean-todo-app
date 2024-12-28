from passlib.context import CryptContext

from app.models import Todo, User
from app.storages.base import NewTodo, NewUser, TodoStorage, UserStorage


class TaskManager:
    def __init__(self, repository: TodoStorage):
        self.repository = repository

    def add_task(self, title: str, description: str, is_done: bool = False) -> Todo:
        new_todo = NewTodo(title=title, description=description, is_done=is_done)
        todo = self.repository.add(new_todo)
        return todo

    def get_all_tasks(self) -> list[Todo]:
        return self.repository.get_all()

    def set_task_status(self, task_id: int, is_done: bool):
        task = self.repository.get_task(task_id)
        if task is None:
            raise ValueError("Task not found")
        self.repository.update_status(task_id, is_done)

    def delete_task(self, task_id: int):
        self.repository.delete(task_id)

    def update_task(
        self, task_id: int, title: str = None, description: str = None
    ) -> Todo:
        task = self.repository.get_task(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            self.repository.update(task)
            return task
        else:
            raise ValueError("Task not found")


class UserManager:
    def __init__(self, user_storage: UserStorage):
        self.user_storage = user_storage
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, username: str, email: str, password: str) -> User:
        hashed_password = self.hash_password(password)
        new_user = NewUser(
            username=username, email=email, hashed_password=hashed_password
        )
        return self.user_storage.add_user(new_user)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_user(self, user_id: int) -> User:
        return self.user_storage.get_user(user_id)

    def delete_user(self, user_id: int):
        self.user_storage.delete_user(user_id)

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
            self.user_storage.update_user(user)
            return user
        else:
            raise ValueError("User not found")
