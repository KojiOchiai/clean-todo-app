from typing import Protocol
from app.manager import TaskManager

class TodoInterface(Protocol):
    def __init__(self, task_manager: TaskManager):
        raise NotImplementedError
        
    def run(self):
        raise NotImplementedError 