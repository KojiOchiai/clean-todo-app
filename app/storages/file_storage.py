import os
import json
from app.models import Todo
from app.storages.base import TodoStorage, NewTodo

class FileTodoStorage(TodoStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({"todos": [], "next_id": 1}, file)

    def _load_data(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def get_next_id(self) -> int:
        data = self._load_data()
        current_id = data["next_id"]
        data["next_id"] += 1
        self._save_data(data)
        return current_id

    def add(self, new_todo: NewTodo) -> Todo:
        data = self._load_data()
        todo = Todo(
            id=self.get_next_id(),
            title=new_todo.title,
            description=new_todo.description,
            is_done=new_todo.is_done
        )
        data["todos"].append(todo.__dict__)
        self._save_data(data)
        return todo

    def delete(self, todo_id: int):
        data = self._load_data()
        data["todos"] = [todo for todo in data["todos"] if todo["id"] != todo_id]
        self._save_data(data)

    def get_all(self) -> list[Todo]:
        data = self._load_data()
        return [Todo(**todo) for todo in data["todos"]]

    def update_status(self, todo_id: int, is_done: bool):
        data = self._load_data()
        for todo in data["todos"]:
            if todo["id"] == todo_id:
                todo["is_done"] = is_done
                break
        self._save_data(data)

    def get_task(self, todo_id: int) -> Todo:
        data = self._load_data()
        for todo in data["todos"]:
            if todo["id"] == todo_id:
                return Todo(**todo)
        return None

    def update(self, todo: Todo):
        data = self._load_data()
        for i, t in enumerate(data["todos"]):
            if t["id"] == todo.id:
                data["todos"][i] = todo.__dict__
                break
        self._save_data(data) 