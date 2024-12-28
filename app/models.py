from dataclasses import dataclass


@dataclass
class Todo:
    id: int
    owner_id: int
    title: str
    description: str
    is_done: bool


@dataclass
class User:
    user_id: int
    username: str
    hashed_password: str
    email: str
    disabled: bool
