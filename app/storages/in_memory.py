from app.models import Todo
from app.storages.base import NewTodo, TodoStorage


class InMemoryTodoStorage(TodoStorage):
    def __init__(self):
        self.todos = []
        self.next_id = 1

    def add(self, new_todo: NewTodo) -> Todo:
        todo = Todo(
            id=self.next_id,
            title=new_todo.title,
            description=new_todo.description,
            is_done=new_todo.is_done,
        )
        self.todos.append(todo)
        self.next_id += 1
        return todo

    def delete(self, todo_id: int):
        self.todos = [todo for todo in self.todos if todo.id != todo_id]

    def get_all(self) -> list[Todo]:
        return self.todos

    def update_status(self, todo_id: int, is_done: bool):
        for todo in self.todos:
            if todo.id == todo_id:
                todo.is_done = is_done
                break

    def get_task(self, todo_id: int) -> Todo:
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update(self, todo: Todo):
        for i, t in enumerate(self.todos):
            if t.id == todo.id:
                self.todos[i] = todo
                break
