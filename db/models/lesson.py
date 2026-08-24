from sqlmodel import Field, SQLModel

class Lesson(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  class_id: int | None = Field(default=None, foreign_key="class.id")
  name: str