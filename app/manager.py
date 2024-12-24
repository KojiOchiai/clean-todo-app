from app.models import Todo
from app.storages.base import TodoStorage

class TaskManager:
    def __init__(self, repository: TodoStorage):
        self.repository = repository

    def add_task(self, title: str, description: str, is_done: bool = False):
        new_todo = Todo(
            id=self.repository.get_next_id(),
            title=title,
            description=description,
            is_done=is_done
        )
        self.repository.add(new_todo)

    def get_all_tasks(self) -> list[Todo]:
        return self.repository.get_all()

    def set_task_status(self, task_id: int, is_done: bool):
        self.repository.update_status(task_id, is_done)

    def delete_task(self, task_id: int):
        self.repository.delete(task_id)
