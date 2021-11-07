from pydantic import BaseModel, EmailStr
from datetime import datetime

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

class UserLogin(UserBase):
  ...