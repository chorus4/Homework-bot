from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
  id: int = Field(primary_key=True)
  username: str
  role: str | None = Field(default='user')