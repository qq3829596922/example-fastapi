from fastapi import status,HTTPException,Depends,APIRouter,Response
from sqlalchemy.orm import Session
from app.utils import verify
from ..database import get_db
from .. import models,oauth2
from ..schema import UserLogin,Token
from fastapi.security import OAuth2PasswordRequestForm


router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)



@router.post("/login",response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    print(user_credentials)
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user not found")
    if not verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="password is incorrect")
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}
