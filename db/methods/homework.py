from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.homework import Homework

session = Session(engine)

def get_homework(id: int) -> Homework:
  homework = session.exec(select(Homework).where(Homework.id == id)).first()
  return homework

def get_homeworks(class_id: int):
  homeworks = session.exec(select(Homework).where(Homework.class_id == class_id)).all()
  return homeworks

def create_homework(class_id, lesson_id, date, content):
  homework = Homework(class_id=class_id, lesson_id=lesson_id, date=date, content=content)
  session.add(homework)
  session.commit()