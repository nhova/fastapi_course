from pydantic import BaseModel
from pydantic.types import conint

class VoteBase(BaseModel):
  post_id: int
  voted: bool

class VoteCreate(VoteBase):
  ...

class VoteUpdate(VoteBase):
  ...

# class VoteResponse(VoteBase):
  # ...

#   class Config:
#     orm_mode = True