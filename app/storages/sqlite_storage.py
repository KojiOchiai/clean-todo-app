from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.models import Todo, User
from app.storages.base import NewTodo, NewUser, TodoStorage, UserStorage

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)


class SQLiteUserStorage(UserStorage):
    def __init__(self, session_local):
        self.SessionLocal = session_local

    def add_user(self, new_user: NewUser) -> User:
        session = self.SessionLocal()
        user_model = UserModel(
            username=new_user.username,
            email=new_user.email,
            hashed_password=new_user.hashed_password,
            disabled=False,
        )
        session.add(user_model)
        session.commit()
        session.refresh(user_model)
        session.close()
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            disabled=user_model.disabled,
        )

    def delete_user(self, user_id: int) -> None:
        session = self.SessionLocal()
        session.query(UserModel).filter(UserModel.id == user_id).delete()
        session.commit()
        session.close()

    def get_user_by_id(self, user_id: int) -> User | None:
        session = self.SessionLocal()
        user = session.query(UserModel).filter(UserModel.id == user_id).first()
        session.close()
        if user:
            return User(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                disabled=user.disabled,
            )
        return None

    def get_user_by_username(self, username: str) -> User | None:
        session = self.SessionLocal()
        user = session.query(UserModel).filter(UserModel.username == username).first()
        session.close()
        if user:
            return User(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                disabled=user.disabled,
            )
        return None

    def get_user_by_email(self, email: str) -> User | None:
        session = self.SessionLocal()
        user = session.query(UserModel).filter(UserModel.email == email).first()
        session.close()
        if user:
            return User(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                disabled=user.disabled,
            )
        return None

    def get_all_users(self) -> list[User]:
        session = self.SessionLocal()
        users = session.query(UserModel).all()
        session.close()
        return [
            User(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                disabled=user.disabled,
            )
            for user in users
        ]

    def update_user(self, user: User) -> User | None:
        session = self.SessionLocal()
        user_model = session.query(UserModel).filter(UserModel.id == user.id).first()
        if user_model:
            user_model.username = user.username
            user_model.email = user.email
            user_model.hashed_password = user.hashed_password
            user_model.disabled = user.disabled
            session.commit()
            session.close()
            return user
        session.close()
        return None


class SQLiteTodoStorage(TodoStorage):
    def __init__(self, session_local):
        self.SessionLocal = session_local

    def add(self, new_todo: NewTodo) -> Todo:
        session = self.SessionLocal()
        todo_model = TodoModel(
            user_id=new_todo.user_id,
            title=new_todo.title,
            description=new_todo.description,
            is_done=new_todo.is_done,
        )
        session.add(todo_model)
        session.commit()
        session.refresh(todo_model)
        session.close()
        return Todo(
            id=todo_model.id,
            user_id=todo_model.user_id,
            title=todo_model.title,
            description=todo_model.description,
            is_done=todo_model.is_done,
        )

    def delete(self, todo_id: int):
        session = self.SessionLocal()
        session.query(TodoModel).filter(TodoModel.id == todo_id).delete()
        session.commit()
        session.close()

    def get_tasks_by_user_id(self, user_id: int) -> list[Todo]:
        session = self.SessionLocal()
        todos = session.query(TodoModel).filter(TodoModel.user_id == user_id).all()
        session.close()
        return [
            Todo(
                id=todo.id,
                user_id=todo.user_id,
                title=todo.title,
                description=todo.description,
                is_done=todo.is_done,
            )
            for todo in todos
        ]

    def get_task_by_id(self, todo_id: int) -> Todo | None:
        session = self.SessionLocal()
        todo = session.query(TodoModel).filter(TodoModel.id == todo_id).first()
        session.close()
        if todo:
            return Todo(
                id=todo.id,
                user_id=todo.user_id,
                title=todo.title,
                description=todo.description,
                is_done=todo.is_done,
            )
        return None

    def update_status(self, todo_id: int, is_done: bool) -> Todo | None:
        session = self.SessionLocal()
        todo = session.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if todo:
            todo.is_done = is_done
            session.commit()
            session.refresh(todo)
            session.close()
            return Todo(
                id=todo.id,
                user_id=todo.user_id,
                title=todo.title,
                description=todo.description,
                is_done=todo.is_done,
            )
        session.close()
        return None

    def update(self, todo: Todo) -> Todo | None:
        session = self.SessionLocal()
        todo_model = session.query(TodoModel).filter(TodoModel.id == todo.id).first()
        if todo_model:
            todo_model.title = todo.title
            todo_model.description = todo.description
            todo_model.is_done = todo.is_done
            session.commit()
            session.refresh(todo_model)
            session.close()
            return todo
        session.close()
        return None


def get_sqlite_storage(
    db_url: str = "sqlite:///app.db",
) -> tuple[SQLiteUserStorage, SQLiteTodoStorage]:
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SQLiteUserStorage(SessionLocal), SQLiteTodoStorage(SessionLocal)
