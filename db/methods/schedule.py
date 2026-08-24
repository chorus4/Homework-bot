from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.schedule import SCEntry

session = Session(engine)

def get_entry(id) -> SCEntry:
  entry = session.exec(select(SCEntry).where(SCEntry.id == id)).first()
  return entry

def create_entry(day_num, class_id, lesson_id, position):
  entry = SCEntry(day_num=day_num, class_id=class_id, lesson_id=lesson_id, position=position)
  session.add(entry)
  session.commit()

def get_entries_by_lesson_dif_day(lesson_id) -> list[SCEntry]:
  entries = session.exec(
    select(SCEntry)
      .where(SCEntry.lesson_id == lesson_id)
      .distinct(SCEntry.lesson_id)
    ).all()
  return entries
