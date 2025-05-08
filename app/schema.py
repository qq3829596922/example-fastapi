from pydantic import BaseModel, Field,EmailStr
from typing import Optional,Union, Annotated
from datetime import datetime
from pydantic.types import conint

class post(BaseModel):
    id:Optional[int] = None 
    title:str
    content:str
    published:Optional[bool] = Field(default=False)
    created_at:Optional[datetime] = Field(default_factory=datetime.now)
    owner_id:int
    class Config:
        from_attributes=True

class updatePost(BaseModel):
    title:str
    content:str
    published:Optional[bool] = Field(default=False)

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes=True

class postResponse(BaseModel):
    id:int
    title:str
    content:str
    owner_id:int
    owner:UserResponse
    published:bool
    class Config:
        from_attributes=True

class post_vote_Response(BaseModel):
    Post:postResponse
    votes:int
    class Config:
        from_attributes=True


class createPost(BaseModel):
    title:str
    content:str
    published:Optional[bool] = Field(default=False)
    # owner_id:int

class User(BaseModel):
    id:Union[int,None] = None
    email:EmailStr
    password:str
    created_at:Union[datetime,None] = None
    class Config:
        from_attributes=True

        
class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str | None = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]  # 0表示取消点赞，1表示点赞

