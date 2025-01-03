from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.manager import TaskManager, UserManager
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TodoModel(BaseModel):
    title: str
    description: str
    is_done: bool = False


class UserModel(BaseModel):
    username: str
    email: str
    password: str


class TodoWebUI:
    def __init__(self, user_manager: UserManager, task_manager: TaskManager):
        self.user_manager = user_manager
        self.task_manager = task_manager
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="app/ui/templates")
        self._setup_routes()

    def _get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        try:
            return self.user_manager.get_user_by_token(token)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    def _setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def read_root(
            request: Request, user: User = Depends(self._get_current_user)
        ):
            todos = self.task_manager.get_tasks_by_user_id(user.id)
            return self.templates.TemplateResponse(
                "index.html", {"request": request, "todos": todos}
            )

        @self.app.post("/token")
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            try:
                token = self.user_manager.login(form_data.username, form_data.password)
                return {"access_token": token, "token_type": "bearer"}
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                )

        @self.app.post("/user", status_code=201)
        async def add_user(user: UserModel):
            try:
                new_user = self.user_manager.create_user(
                    user.username, user.email, user.password
                )
                token = self.user_manager.login(user.username, user.password)
                return {
                    "message": "User created successfully",
                    "username": new_user.username,
                    "token": token,
                    "token_type": "bearer",
                }
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                )

        @self.app.put("/user", status_code=200)
        async def update_user(
            user: UserModel,
            current_user: User = Depends(self._get_current_user),
        ):
            try:
                updated_user = self.user_manager.update_user(
                    current_user.id, user.username, user.email, user.password
                )
                return {
                    "message": "User updated successfully",
                    "user": updated_user.__dict__,
                }
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                )

        @self.app.delete("/user", status_code=204)
        async def delete_user(current_user: User = Depends(self._get_current_user)):
            try:
                self.user_manager.delete_user(current_user.id)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                )

        @self.app.get("/todos")
        def list_todos(user: User = Depends(self._get_current_user)):
            todos = self.task_manager.get_tasks_by_user_id(user.id)
            return [todo.__dict__ for todo in todos]

        @self.app.post("/todo", status_code=201)
        def add_todo(item: TodoModel, user: User = Depends(self._get_current_user)):
            new_todo = self.task_manager.create_task(
                user.id, item.title, item.description, item.is_done
            )
            return {"message": "Todo added successfully", "todo": new_todo.__dict__}

        @self.app.put("/todo/{todo_id}")
        def update_todo(
            todo_id: int,
            item: TodoModel,
            user: User = Depends(self._get_current_user),
        ):
            try:
                updated_task = self.task_manager.update_task(
                    user.id, todo_id, item.title, item.description
                )
                if item.is_done is not None:
                    self.task_manager.set_task_status(user.id, todo_id, item.is_done)
                return {
                    "message": "Todo updated successfully",
                    "todo": updated_task.__dict__,
                }
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))

        @self.app.delete("/todo/{todo_id}", status_code=204)
        def delete_todo(todo_id: int, user: User = Depends(self._get_current_user)):
            try:
                self.task_manager.delete_task(user.id, todo_id)
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))

    def run(self):
        import uvicorn

        uvicorn.run(self.app, host="0.0.0.0", port=8000)
