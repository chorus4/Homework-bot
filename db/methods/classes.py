from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.classes import Class
from db.methods.access import create_access, get_accesses_by_user, get_accesses_by_class

from functools import singledispatch

session = Session(engine)

def create_class(owner, name):
  classs = Class(owner=owner, name=name)
  session.add(classs)
  session.commit()
  create_access(classs.id, owner, "owner")

@singledispatch
def get_class(arg) -> Class:
  print("fuck")

@get_class.register
def _(id: int):
  classs = session.exec(select(Class).where(Class.id == id)).first()
  return classs

@get_class.register
def _(name: str):
  classs = session.exec(select(Class).where(Class.name == name)).first()
  return classs

def get_classes(user_id) -> list[Class]:
  accesses = get_accesses_by_user(user_id)
  classes = []
  for access in accesses:
    cls = session.exec(select(Class).where(Class.id == access.class_id)).all()
    for class_ in cls:
      classes.append(class_)

  return classes

def delete_class(class_id: int):
  classs = get_class(class_id)
  accesses = get_accesses_by_class(class_id)
  for access in accesses:
    session.delete(access)
  session.delete(classs)
  session.commit()

def get_class_by_link(link):
  classs = session.exec(select(Class).where(Class.link == link)).first()
  return classs