from app.models import Todo
from dataclasses import dataclass

@dataclass
class NewTodo:
    title: str
    description: str
    is_done: bool = False 

class TodoStorage:
    def add(self, new_todo: NewTodo) -> Todo:
        raise NotImplementedError

    def delete(self, todo_id: int):
        raise NotImplementedError

    def get_all(self) -> list[Todo]:
        raise NotImplementedError

    def update_status(self, todo_id: int, is_done: bool):
        raise NotImplementedError

    def get_task(self, todo_id: int) -> Todo:
        raise NotImplementedError

    def update(self, todo: Todo):
        raise NotImplementedError