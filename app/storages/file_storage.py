import json
import os
import pathlib

from app.models import Todo, User
from app.storages.base import NewTodo, NewUser, TodoStorage, UserStorage


class FileUserStorage(UserStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump({"users": [], "next_id": 1}, file)

    def _load_data(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def add_user(self, new_user: NewUser) -> User:
        data = self._load_data()
        user = User(
            id=data["next_id"],
            username=new_user.username,
            hashed_password=new_user.hashed_password,
            email=new_user.email,
            disabled=False,
        )
        data["users"].append(user.__dict__)
        data["next_id"] += 1
        self._save_data(data)
        return user

    def delete_user(self, user_id: int) -> None:
        data = self._load_data()
        data["users"] = [user for user in data["users"] if user["id"] != user_id]
        self._save_data(data)

    def get_user_by_id(self, user_id: int) -> User | None:
        data = self._load_data()
        for user in data["users"]:
            if user["id"] == user_id:
                return User(**user)
        return None

    def get_user_by_username(self, username: str) -> User | None:
        data = self._load_data()
        for user in data["users"]:
            if user["username"] == username:
                return User(**user)
        return None

    def get_user_by_email(self, email: str) -> User | None:
        data = self._load_data()
        for user in data["users"]:
            if user["email"] == email:
                return User(**user)
        return None

    def get_all_users(self) -> list[User]:
        data = self._load_data()
        return [User(**user) for user in data["users"]]

    def update_user(self, user: User) -> User | None:
        data = self._load_data()
        for i, u in enumerate(data["users"]):
            if u["id"] == user.id:
                data["users"][i] = user.__dict__
                self._save_data(data)
                return user
        return None


class FileTodoStorage(TodoStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump({"todos": [], "next_id": 1}, file)

    def _load_data(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def add(self, new_todo: NewTodo) -> Todo:
        data = self._load_data()
        todo = Todo(
            id=data["next_id"],
            user_id=new_todo.user_id,
            title=new_todo.title,
            description=new_todo.description,
            is_done=new_todo.is_done,
        )
        data["todos"].append(todo.__dict__)
        data["next_id"] += 1
        self._save_data(data)
        return todo

    def delete(self, todo_id: int):
        data = self._load_data()
        data["todos"] = [todo for todo in data["todos"] if todo["id"] != todo_id]
        self._save_data(data)

    def get_tasks_by_user_id(self, user_id: int) -> list[Todo]:
        data = self._load_data()
        return [Todo(**todo) for todo in data["todos"] if todo["user_id"] == user_id]

    def get_task_by_id(self, todo_id: int) -> Todo | None:
        data = self._load_data()
        for todo in data["todos"]:
            if todo["id"] == todo_id:
                return Todo(**todo)
        return None

    def update_status(self, todo_id: int, is_done: bool):
        data = self._load_data()
        for todo in data["todos"]:
            if todo["id"] == todo_id:
                todo["is_done"] = is_done
                break
        self._save_data(data)

    def update(self, todo: Todo):
        data = self._load_data()
        for i, t in enumerate(data["todos"]):
            if t["id"] == todo.id:
                data["todos"][i] = todo.__dict__
                break
        self._save_data(data)


def get_file_storage(dir_path: str) -> tuple[FileUserStorage, FileTodoStorage]:
    path = pathlib.Path(dir_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    user_file_path = path / "user_data.json"
    todo_file_path = path / "todo_data.json"
    return (
        FileUserStorage(file_path=user_file_path),
        FileTodoStorage(file_path=todo_file_path),
    )
