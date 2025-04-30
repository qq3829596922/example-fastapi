from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from app.schema import TokenData
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    # print(to_encode)
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    # print(encoded_jwt)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    # print(token)
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("user_id")
        expire=payload.get("exp")
        print(username)
        print(expire)
        print(datetime.fromtimestamp(expire))
        if username is None:
            raise credentials_exception
        token_data=TokenData(username=str(username))
        # print(token_data,"token_data")
        return int(token_data.username)
    except JWTError:
        raise credentials_exception

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token).first()
    print(user,"from oauth2.py get_current_user")
    return user.id

