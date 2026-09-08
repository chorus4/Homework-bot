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

def get_entries_by_lesson_dif_day(class_id, lesson_id) -> list[SCEntry]:
  entries = session.exec(
    select(SCEntry)
      .where(SCEntry.class_id == class_id).where(SCEntry.lesson_id == lesson_id)
      .order_by(SCEntry.day_num)
    ).all()
  seen_days = set()
  unique_records = []
  for record in entries:
      if record.day_num not in seen_days:
          seen_days.add(record.day_num)
          unique_records.append(record)
  return unique_records

def get_entries_by_day(day_num, class_id) -> list[SCEntry]:
  entry = session.exec(select(SCEntry).where(SCEntry.day_num == day_num).where(SCEntry.class_id == class_id).order_by(SCEntry.position)).all()
  return entry

def check_entry_by_pos(class_id, day_num, position):
  entry = session.exec(select(SCEntry).where(SCEntry.position == position).where(SCEntry.class_id == class_id).where(SCEntry.day_num == day_num).order_by(SCEntry.position)).first()
  return entry != None

def change_entry(class_id, day_num, position, lesson_id):
  if check_entry_by_pos(class_id, day_num, position):
    entry = session.exec(select(SCEntry).where(SCEntry.position == position).where(SCEntry.class_id == class_id).where(SCEntry.day_num == day_num).order_by(SCEntry.position)).first()
    entry.lesson_id = lesson_id
    session.add(entry)
    session.commit()

  else:
    entry = SCEntry(class_id=class_id, day_num=day_num, position=position, lesson_id=lesson_id)
    session.add(entry)
    session.commit()

def delete_entry(class_id, day_num, position):
  if not check_entry_by_pos(class_id, day_num, position): return
  entry = session.exec(select(SCEntry).where(SCEntry.position == position).where(SCEntry.class_id == class_id).where(SCEntry.day_num == day_num).order_by(SCEntry.position)).first()
  session.delete(entry)
  session.commit()