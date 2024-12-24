from app.models import Todo
from app.storages.base import TodoStorage

class InMemoryTodoStorage(TodoStorage):
    def __init__(self):
        self.todos = []
        self.next_id = 1

    def get_next_id(self) -> int:
        current_id = self.next_id
        self.next_id += 1
        return current_id

    def add(self, todo: Todo):
        self.todos.append(todo)

    def get_all(self) -> list[Todo]:
        return self.todos

    def update_status(self, todo_id: int, is_done: bool):
        for todo in self.todos:
            if todo.id == todo_id:
                todo.is_done = is_done
                break 

    def delete(self, todo_id: int):
        self.todos = [todo for todo in self.todos if todo.id != todo_id] 