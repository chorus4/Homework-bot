from sqlmodel import Field, SQLModel
from datetime import date

class Homework(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  class_id: int | None = Field(foreign_key="class.id")
  lesson_id: int | None = Field(foreign_key="lesson.id")
  date: date
  content: str