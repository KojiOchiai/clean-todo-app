from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.manager import TaskManager

app = FastAPI()

class TodoItem(BaseModel):
    title: str
    description: str
    is_done: bool = False

class TodoWebUI:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self._setup_routes()

    def _setup_routes(self):
        @app.get("/todos")
        def list_todos():
            todos = self.task_manager.get_all_tasks()
            return [todo.__dict__ for todo in todos]

        @app.post("/todos", status_code=201)
        def add_todo(item: TodoItem):
            self.task_manager.add_task(item.title, item.description, item.is_done)
            return {"message": "Todo added successfully"}

        @app.put("/todos/{todo_id}")
        def update_todo_status(todo_id: int, is_done: bool):
            try:
                self.task_manager.set_task_status(todo_id, is_done)
                return {"message": "Todo status updated successfully"}
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))

        @app.delete("/todos/{todo_id}", status_code=204)
        def delete_todo(todo_id: int):
            try:
                self.task_manager.delete_task(todo_id)
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))

    def run(self):
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000) 