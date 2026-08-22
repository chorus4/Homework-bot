from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.classes import Class

from functools import singledispatch

session = Session(engine)

def create_class(owner, name):
  classs = Class(owner=owner, name=name)
  session.add(classs)
  session.commit()

@singledispatch
def get_class(arg):
  print("fuck")

@get_class.register
def _(id: int):
  classs = session.exec(select(Class).where(Class.id == id)).first()
  return classs

@get_class.register
def _(name: str):
  classs = session.exec(select(Class).where(Class.name == name)).first()
  return classs

def get_classes(user_id):
  classes = session.exec(select(Class).where(Class.owner == user_id)).all()
  return classes