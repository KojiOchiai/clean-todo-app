from app.models import Todo
from app.storages.base import TodoStorage

class TaskManager:
    def __init__(self, repository: TodoStorage):
        self.repository = repository

    def add_task(self, title: str, description: str, is_done: bool = False) -> Todo:
        new_todo = Todo(
            id=self.repository.get_next_id(),
            title=title,
            description=description,
            is_done=is_done
        )
        self.repository.add(new_todo)
        return new_todo

    def get_all_tasks(self) -> list[Todo]:
        return self.repository.get_all()

    def set_task_status(self, task_id: int, is_done: bool):
        task = self.repository.get_task(task_id)
        if task is None:
            raise ValueError("Task not found")
        self.repository.update_status(task_id, is_done)

    def delete_task(self, task_id: int):
        self.repository.delete(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Todo:
        task = self.repository.get_task(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            self.repository.update(task)
            return task
        else:
            raise ValueError("Task not found")
