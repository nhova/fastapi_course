from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.user import UserModel
from app.misc.utils import verify_hash
from app.misc.oauth2 import create_access_token
from app.schemas.user import Token

router = APIRouter(
  tags = ["Authentication"]
)

@router.post("/login", response_model=Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(UserModel).filter(UserModel.email == user_creds.username).first()
  if user:
    if verify_hash(user_creds.password, user.password):
      access_token = create_access_token(data = {"user_id": user.id})
      return {"access_token": access_token, "token_type": "bearer"}
  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail=f"Invalid credentials") 
