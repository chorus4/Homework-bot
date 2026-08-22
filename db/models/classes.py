from sqlmodel import Field, SQLModel

import uuid

class Class(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  owner: int
  name: str
  link: uuid.UUID | None = Field(default_factory=uuid.uuid4)