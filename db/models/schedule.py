from sqlmodel import Field, SQLModel

class SCEntry(SQLModel, table=True): # Schedule entry
  id: int | None = Field(default=None, primary_key=True)
  day_num: int # Number of day (starts from Monday)
  position: int
  class_id: int | None = Field(default=None, foreign_key="class.id")
  lesson_id: int = Field(foreign_key='lesson.id')