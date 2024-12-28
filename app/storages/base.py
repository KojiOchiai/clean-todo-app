from dataclasses import dataclass

from app.models import Todo, User


@dataclass
class NewTodo:
    user_id: int
    title: str
    description: str
    is_done: bool = False


@dataclass
class NewUser:
    username: str
    email: str
    hashed_password: str


class TodoStorage:
    def add(self, new_todo: NewTodo) -> Todo:
        raise NotImplementedError

    def delete(self, todo_id: int):
        raise NotImplementedError

    def get_all(self) -> list[Todo]:
        raise NotImplementedError

    def get_all_by_user_id(self, user_id: int) -> list[Todo]:
        raise NotImplementedError

    def update_status(self, todo_id: int, is_done: bool):
        raise NotImplementedError

    def get_task(self, todo_id: int) -> Todo:
        raise NotImplementedError

    def update(self, todo: Todo):
        raise NotImplementedError


class UserStorage:
    def add_user(self, new_user: NewUser) -> User:
        raise NotImplementedError

    def delete_user(self, user_id: int) -> None:
        raise NotImplementedError

    def get_user(self, user_id: int) -> User:
        raise NotImplementedError

    def get_user_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> User:
        raise NotImplementedError

    def get_all_users(self) -> list[User]:
        raise NotImplementedError

    def update_user(self, user: User) -> None:
        raise NotImplementedError
