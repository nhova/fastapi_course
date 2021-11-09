from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base

class VoteModel(Base):
  __tablename__ = "votes"
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)