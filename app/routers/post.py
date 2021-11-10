from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from app.models.vote import VoteModel
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostOut
from app.schemas.user import UserResponse
from app.database.base import get_db
from app.models.post import PostModel
from app.misc.oauth2 import get_current_user

router = APIRouter(
  prefix = "/posts",
  tags = ["Posts"]
)

@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    #posts = db.query(PostModel).filter(PostModel.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(PostModel, func.count(VoteModel.post_id).label("votes")).join(VoteModel, VoteModel.post_id == PostModel.id, isouter=True).group_by(PostModel.id).filter(
              PostModel.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}" , response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
  post = db.query(PostModel).filter(PostModel.id == id).first()

  post = db.query(PostModel, func.count(VoteModel.post_id).label("votes")).join(VoteModel, VoteModel.post_id == PostModel.id, isouter=True).group_by(PostModel.id).filter(
            PostModel.id == id).first()

  if post:
    return post
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} was not found.") 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
  new_post = PostModel(owner_id=current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
  post = db.query(PostModel).filter(PostModel.id == id)
  post_result = post.first()
  
  if post_result == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} was not found.")
  if post_result.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")
  
  post.delete(synchronize_session=False)
  db.commit()     

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
  post_query = db.query(PostModel).filter(PostModel.id == id)
  post = post_query.first()

  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} was not found.")
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")
 
  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()
  return post_query.first()