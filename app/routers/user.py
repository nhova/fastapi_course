from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.database.base import get_db
from app.models.user import UserModel
from app.misc.utils import make_hash
from app.misc.oauth2 import get_current_user

router = APIRouter(
  prefix = "/users",
  tags = ["Users"]
)

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    users = db.query(UserModel).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  user.password = make_hash(user.password)
  new_user = UserModel(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@router.get("/{id}" , response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
  user = db.query(UserModel).filter(UserModel.id == id).first()
  if user:
    return user
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} was not found.") 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
  user = db.query(UserModel).filter(UserModel.id == id)
  if user.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} was not found.")
  else:
    user.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}", response_model=UserResponse)
def update_user(id: int, updated_user: UserUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
  user_query = db.query(UserModel).filter(UserModel.id == id)
  user = user_query.first()
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Post with id: {id} was not found.")
  else:
    updated_user.password = make_hash(updated_user.password)
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()
