import datetime

import jwt
from passlib.context import CryptContext

from app.models import Todo, User
from app.storages.base import NewTodo, NewUser, TodoStorage, UserStorage


class TaskManager:
    def __init__(self, storage: TodoStorage):
        self.storage = storage

    def create_task(
        self, user_id: int, title: str, description: str, is_done: bool = False
    ) -> Todo:
        new_todo = NewTodo(
            user_id=user_id, title=title, description=description, is_done=is_done
        )
        todo = self.storage.add(new_todo)
        return todo

    def get_tasks_by_user_id(self, user_id: int) -> list[Todo]:
        return self.storage.get_tasks_by_user_id(user_id)

    def set_task_status(self, user_id: int, task_id: int, is_done: bool) -> None:
        task = self.storage.get_task(task_id)
        if task is None or task.user_id != user_id:
            raise ValueError("Task not found")
        self.storage.update_status(task_id, is_done)

    def delete_task(self, user_id: int, task_id: int) -> None:
        task = self.storage.get_task(task_id)
        if task is None or task.user_id != user_id:
            raise ValueError("Task not found")
        self.storage.delete(task_id)

    def update_task(
        self, user_id: int, task_id: int, title: str = None, description: str = None
    ) -> Todo:
        task = self.storage.get_task(task_id)
        if task is None or task.user_id != user_id:
            raise ValueError("Task not found")
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        self.storage.update(task)
        return task


class UserManager:
    def __init__(self, user_storage: UserStorage, secret_key: str):
        self.storage = user_storage
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = secret_key

    def create_user(self, username: str, email: str, password: str) -> User:
        if self.storage.get_user_by_email(email):
            raise ValueError("User already exists")
        hashed_password = self.hash_password(password)
        new_user = NewUser(
            username=username, email=email, hashed_password=hashed_password
        )
        return self.storage.add_user(new_user)

    def login(self, email: str, password: str) -> str:
        user = self.authenticate_user(email, password)
        return self.create_access_token(user.id)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.storage.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        return user

    def create_access_token(
        self, user_id: int, expires_delta: datetime.timedelta = None
    ) -> str:
        to_encode = {"user_id": user_id}
        if not expires_delta:
            expires_delta = datetime.timedelta(minutes=15)
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm="HS256")
        return encoded_jwt

    def get_user_by_token(self, token: str) -> User:
        user_id = self.verify_access_token(token)
        return self.storage.get_user_by_id(user_id)

    def verify_access_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise ValueError("Invalid token")
            return user_id
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.JWTError:
            raise ValueError("Invalid token")

    def get_user_by_id(self, user_id: int) -> User:
        return self.storage.get_user_by_id(user_id)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

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
