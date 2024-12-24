from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models import Todo
from app.storages.base import TodoStorage, NewTodo

Base = declarative_base()

class TodoModel(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)

class SQLiteTodoStorage(TodoStorage):
    def __init__(self, db_url='sqlite:///todos.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add(self, new_todo: NewTodo) -> Todo:
        session = self.Session()
        todo_model = TodoModel(
            title=new_todo.title,
            description=new_todo.description,
            is_done=new_todo.is_done
        )
        session.add(todo_model)
        session.commit()
        session.refresh(todo_model)
        session.close()
        return Todo(id=todo_model.id, title=todo_model.title, description=todo_model.description, is_done=todo_model.is_done)

    def delete(self, todo_id: int):
        session = self.Session()
        session.query(TodoModel).filter(TodoModel.id == todo_id).delete()
        session.commit()
        session.close()

    def get_all(self) -> list[Todo]:
        session = self.Session()
        todos = session.query(TodoModel).all()
        session.close()
        return [Todo(id=todo.id, title=todo.title, description=todo.description, is_done=todo.is_done) for todo in todos]

    def update_status(self, todo_id: int, is_done: bool):
        session = self.Session()
        todo = session.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if todo:
            todo.is_done = is_done
            session.commit()
        session.close()

    def get_task(self, todo_id: int) -> Todo:
        session = self.Session()
        todo = session.query(TodoModel).filter(TodoModel.id == todo_id).first()
        session.close()
        if todo:
            return Todo(id=todo.id, title=todo.title, description=todo.description, is_done=todo.is_done)
        return None

    def update(self, todo: Todo):
        session = self.Session()
        todo_model = session.query(TodoModel).filter(TodoModel.id == todo.id).first()
        if todo_model:
            todo_model.title = todo.title
            todo_model.description = todo.description
            todo_model.is_done = todo.is_done
            session.commit()
        session.close() 