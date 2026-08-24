from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.lesson import Lesson

session = Session(engine)

def get_lesson(id) -> Lesson:
  lesson = session.exec(select(Lesson).where(Lesson.id == id)).first()
  return lesson

def get_lessons(class_id) -> list[Lesson]:
  lessons = session.exec(select(Lesson).where(Lesson.class_id == class_id)).all()
  return lessons

def create_lesson(class_id, name):
  lesson = Lesson(class_id=class_id, name=name)
  session.add(lesson)
  session.commit()

def delete_lesson(id):
  lesson = get_lesson(id)
  session.delete(lesson)
  session.commit()