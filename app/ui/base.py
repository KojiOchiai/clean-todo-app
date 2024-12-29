from typing import Protocol

from app.manager import TaskManager, UserManager


class TodoInterface(Protocol):
    def __init__(self, user_manager: UserManager, task_manager: TaskManager):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
