from fastapi import Response, status, HTTPException, APIRouter, Depends
from .. import models, schemas, oauth2
from ..database import SessionDep
from sqlmodel import select
from typing import Annotated

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, session: SessionDep,
         current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    
    found_post = session.exec(select(models.Post).filter(models.Post.id == vote.post_id)).first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {vote.post_id} does not exist')
    
    found_vote = session.exec(select(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)).first()

    if vote.direction:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'vote does not exist')
        
        session.delete(found_vote)
        session.commit()
        return {"message": "successfully deleted vote"}
        
    