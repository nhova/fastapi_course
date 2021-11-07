from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import TokenData
from app.database.base import get_db
from app.models.user import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "cec033c9345101077c8497164f4c85d2922c576b6991992bcf0a7f7cded50550"
ALGORITHM = "HS256"
TOKEN_EXPIRE = 90  

def create_access_token(data: dict):
  to_encode = data.copy()
  expiry = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE)
  to_encode.update({"exp": expiry})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, creds_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    id: str = payload.get("user_id")
    if id is None:
      raise creds_exception
    else:
      token_data = TokenData(id=id)
  except JWTError:
    raise creds_exception
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail = "Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
  token_data = verify_access_token(token, creds_exception)
  user = db.query(UserModel).filter(UserModel.id == token_data.id).first()
  return user