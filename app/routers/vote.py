from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.models.vote import VoteModel
from app.models.post import PostModel

from app.schemas.vote import VoteCreate
from app.schemas.user import UserResponse

from app.database.base import get_db
from app.misc.oauth2 import get_current_user

router = APIRouter(
  prefix = "/votes",
  tags = ["Voting"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):

  post = db.query(PostModel).filter(PostModel.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {vote.post_id} was not found.") 

  vote_query = db.query(VoteModel).filter( VoteModel.post_id == vote.post_id, VoteModel.user_id == current_user.id )
  found_vote = vote_query.first()
  if vote.voted:
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                    detail=f"User {current_user.id} has already voted on post {vote.post_id}")
    new_vote = VoteModel(post_id = vote.post_id, user_id = current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "Successfully added vote"}
  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
              detail=f"User {current_user.id} has not voted on post {vote.post_id}")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Successfully removed vote"}

