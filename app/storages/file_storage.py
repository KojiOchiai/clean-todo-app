import os
import json
from app.models import Todo
from app.storages.base import TodoStorage

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
        return data["next_id"]

    def add(self, todo: Todo):
        data = self._load_data()
        data["todos"].append(todo.__dict__)
        data["next_id"] += 1
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

    def delete(self, todo_id: int):
        data = self._load_data()
        data["todos"] = [todo for todo in data["todos"] if todo["id"] != todo_id]
        self._save_data(data) 