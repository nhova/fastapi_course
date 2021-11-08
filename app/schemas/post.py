from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):
  ...

class PostUpdate(PostBase):
  ...

class PostResponse(PostBase):
  id: int
  created_at: datetime
  owner_id: int

  class Config:
    orm_mode = True