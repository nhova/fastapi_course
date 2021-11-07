from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.database.base import Base

class UserBase(BaseModel):
  email: EmailStr
  password: str

class UserCreate(UserBase):
  ...

class UserUpdate(UserBase):
  ...

class UserResponse(BaseModel):
  email: EmailStr
  id: int
  created_at: datetime

  class Config:
    orm_mode = True

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None