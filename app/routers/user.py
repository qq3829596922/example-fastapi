from fastapi import status,HTTPException,Depends
from sqlalchemy.orm import Session
from .. import models,utils
from ..schema import User,UserResponse,UserCreate
from ..database import get_db
from fastapi import APIRouter

router=APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(payload:UserCreate,db:Session=Depends(get_db)):
    try:
        print(payload,"from payload")
        hashed_password=utils.hash(payload.password)
        payload.password=hashed_password
        new_user=models.User(**payload.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"数据库插入失败: {e}")

@router.get("/{id}",response_model=UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id}user not found")
    return user
