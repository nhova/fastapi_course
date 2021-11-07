from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database.base import Base

class UserModel(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String,  nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))