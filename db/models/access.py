from sqlmodel import Field, SQLModel

class Access(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  class_id: int = Field(foreign_key="class.id")
  user_id: int = Field(foreign_key="user.id")
  role: str