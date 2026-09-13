from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.access import Access

session = Session(engine)

def get_access(id) -> Access:
  access = session.exec(select(Access).where(Access.id == id)).first()
  return access

def get_accesses_by_user(user_id) -> list[Access]:
  accesses = session.exec(select(Access).where(Access.user_id == user_id)).all()
  return accesses

def get_accesses_by_class(class_id: int) -> list[Access]:
  accesses = session.exec(select(Access).where(Access.class_id == class_id)).all()
  return accesses

def check_access(user_id: int, class_id: int):
  return get_access_by_all(class_id, user_id) != None

def get_access_by_all(class_id: int, user_id: int) -> Access:
  access = session.exec(select(Access).where(Access.class_id == class_id).where(Access.user_id == user_id)).first()
  return access

def create_access(class_id, user_id, role):
  access = Access(class_id=class_id, user_id=user_id, role=role)
  session.add(access)
  session.commit()

def delete_access(id):
  access = get_access(id)
  session.delete(access)
  session.commit()