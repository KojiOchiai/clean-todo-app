from app.models import Todo

class TodoStorage:
    def get_next_id(self) -> int:
        raise NotImplementedError

    def add(self, todo: Todo):
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