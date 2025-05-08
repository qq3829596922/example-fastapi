from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.oauth2 import get_current_user
from app.schema import Vote
router=APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:Vote,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    
    try:
        post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
        vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user)
        
        found_vote=vote_query.first()

        if vote.dir==1:
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user} has already voted on post {vote.post_id}")
            new_vote=models.Vote(post_id=vote.post_id,user_id=current_user)
            db.add(new_vote)
            db.commit()
            return {"message":"successfully added vote"}
        else:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message":"successfully deleted vote"}
    except Exception as e:
        raise e

