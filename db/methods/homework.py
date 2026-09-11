from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.homework import Homework
from db.methods.classes import get_class

from datetime import date

session = Session(engine)

def get_homework(id: int) -> Homework:
  homework = session.exec(select(Homework).where(Homework.id == id)).first()
  return homework

def get_homeworks(class_id: int) -> list[Homework]:
  homeworks = session.exec(select(Homework).where(Homework.class_id == class_id)).all()
  return homeworks

def get_homeworks_by_day(class_id: int, day: date) -> list[Homework]:
  homeworks = session.exec(select(Homework).where(Homework.class_id == class_id).where(Homework.date == day)).all()
  return homeworks

def create_homework(class_id, lesson_id, date, content):
  homework = Homework(class_id=class_id, lesson_id=lesson_id, date=date, content=content)
  session.add(homework)
  session.commit()

def delete_homework(homework_id: int):
  homework = get_homework(homework_id)
  session.delete(homework)
  session.commit()

def check_owner(homework_id, user_id):
  homework = get_homework(homework_id)
  classs = get_class(homework.class_id)
  return classs.owner == user_id

def edit_homework_content(homework_id: int, content: str):
  homework = get_homework(homework_id)
  homework.content = content
  session.add(homework)
  session.commit()