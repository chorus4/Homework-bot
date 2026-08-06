from sqlmodel import Session
from sqlmodel import select
from db import engine
from db.models.user import User

session = Session(engine)

def add_user(id, username):
  user = User(id=id, username=username)
  session.add(user)
  session.commit()

def get_user(id: int): 
  user = session.exec(select(User).where(User.id == id)).first()
  return user

def check_user(id):
  return get_user(id) != None

def update_username(id, username):
  user = get_user(id)

  user.username = username
  session.add(user)
  session.commit()

def update_role(id, role):
  user = get_user(id)
  
  user.role = role
  session.add(user)
  session.commit()