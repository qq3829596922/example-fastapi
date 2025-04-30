from fastapi import status,HTTPException,Depends,APIRouter,Response
from sqlalchemy.orm import Session
from .. import models
from sqlalchemy import func
from ..schema import post,updatePost,postResponse,createPost,post_vote_Response
from ..database import get_db
from typing import List,Optional
from ..oauth2 import get_current_user

router=APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=postResponse)
def create_post(payload:createPost,db:Session=Depends(get_db),user_id=Depends(get_current_user)):
    # print("函数开始执行了")
    # print("用户ID:", user_id if user_id else "无用户")
    # print("载荷内容:", payload.model_dump())
    try:
        # 不直接修改payload，而是创建新字典
        # print(user_id,"from user_id")
        post_data = payload.model_dump()
        # print(post_data,"from post_data")
        post_data["owner_id"] = user_id
        # print(post_data,"from post_data")
        # 使用新字典创建Post对象
        new_post=models.Post(**post_data)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        # print("帖子创建成功:", new_post)
        return new_post
    except Exception as e:
        print("错误发生:", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"数据库插入失败: {e}")



@router.get("/",response_model=List[post_vote_Response])
def get_posts(db:Session=Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]="",user_id=Depends(get_current_user)):
    # print(limit,"from limit")
    # print(search,"from search")
    
        # cursor.execute("""SELECT * FROM posts""")
        # # print(cursor)
        # posts = cursor.fetchall()
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.\
    query(models.Post, func.count(models.Vote.post_id).\
    label("votes")).\
    join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).\
    group_by(models.Post.id).\
    filter(models.Post.title.contains(search)).\
    limit(limit).\
    offset(skip).\
    all()

    formatted_results = []
    for post, votes in results:
        # 确保 Post 对象有 votes 属性（Pydantic 模型需要）
        post.votes = votes
        # 创建符合 post_vote_Response 模型的字典
        formatted_results.append({"Post":post,"votes":votes})


    return formatted_results
    # return a



 

@router.get("/latest")
def get_latest_post(db:Session=Depends(get_db)):
    try:
        post=db.query(models.Post).order_by(models.Post.id.desc()).first()
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"数据库查询失败: {e}")


@router.get("/{id}",response_model=post_vote_Response)
def get_post(id:int,db:Session=Depends(get_db),status_code=status.HTTP_200_OK,user_id=Depends(get_current_user)):
    print("dsadasd")
    print(id)  
    post= db.\
    query(models.Post, func.count(models.Vote.post_id).\
    label("votes")).\
    join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).\
    group_by(models.Post.id).\
    filter(models.Post.id==id).\
    first()
    # post.update({"owner_id":user_id})
    # post.user_id=user_id

    # post_dict = post.__dict__.copy()
    # post_dict["user_id"] = user_id
    # hello=postResponse.model_validate(post)

    # print(hello)
    response_post={}
    response_post["Post"]=post[0]
    response_post["votes"]=post[1]

    # post_dict=post.__dict__.copy()

    # print(post_dict,"from post_dict--------------------")

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    print(post,"from post")
    return response_post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user_id=Depends(get_current_user)):
    try:
        post_query=db.query(models.Post).filter(models.Post.id==id)
        post=post_query.first()
        
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
        if post.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"数据库删除失败: {e}")

@router.put("/{id}")
def update_post(id:int,payload:updatePost,db:Session=Depends(get_db),user_id=Depends(get_current_user)):
    try:
        
        post_query=db.query(models.Post).filter(models.Post.id==id)
        post=post_query.first()
        print(post)
        # return post
        # payload.id=id
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
        # print(payload)
        if post.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
        post_query.update(payload.model_dump(),synchronize_session=False)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"数据库更新失败: {e}")
