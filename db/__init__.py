from sqlmodel import SQLModel, create_engine

from env import USE_LOCAL_DB, get_database_url
from db.models import access, classes, homework, lesson, schedule, user  # noqa: F401

connect_args = {"check_same_thread": False} if USE_LOCAL_DB else {}
engine = create_engine(get_database_url(), connect_args=connect_args)


def init():
    SQLModel.metadata.create_all(engine)
