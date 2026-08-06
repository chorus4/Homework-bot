from sqlmodel import Field, SQLModel

class Class(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  owner: int
  name: str