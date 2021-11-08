from pydantic import BaseModel
from datetime import datetime

from app.schemas.user import UserResponse

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
  owner: UserResponse

  class Config:
    orm_mode = True