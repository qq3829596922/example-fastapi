from fastapi import FastAPI, Request
from .database import engine, get_db, create_tables
from sqlalchemy.orm import Session
from .routers import post, user, auth,vote
from fastapi.middleware.cors import CORSMiddleware
# 创建数据库表
create_tables()

app = FastAPI()

# 初始化内存中的帖子列表
# 全局变量

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com",
    "https://www.bilibili.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = None
cursor = None
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
async def root2(request: Request):
    print("请求头:")
    for header, value in request.headers.items():
        print(f"  {header}: {value}")
    
    # 打印请求信息
    print(f"请求方法: {request.method}")
    print(f"请求URL: {request.url}")
    print(f"客户端地址: {request.client.host}:{request.client.port}")
    
    # 如果是表单或JSON数据，可以打印请求体
    try:
        body = await request.body()
        if body:
            print(f"请求体: {body.decode()}")
    except:
        pass
    
    return {"message": "请求信息已在后端控制台打印"}

# # 数据库连接
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost", 
#             database="fastapi", 
#             user="postgres", 
#             password="qq3829596922",  # 使用正确的密码
#             port=5432,
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("数据库连接成功")
        
#         # 检查posts表是否存在
#         cursor.execute("""
#         SELECT EXISTS (
#             SELECT FROM information_schema.tables 
#             WHERE table_schema = 'public' AND table_name = 'posts'
#         );
#         """)
#         table_exists = cursor.fetchone()['exists']
#         print(table_exists)
        
#         # 如果表不存在则创建
#         if not table_exists:
#             cursor.execute("""
#             CREATE TABLE posts (
#                 id SERIAL PRIMARY KEY,
#                 title VARCHAR(255) NOT NULL,
#                 content TEXT NOT NULL,
#                 published BOOLEAN DEFAULT FALSE,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             );
#             """)
#             conn.commit()
#             print("posts表创建成功")
#         break
#     except Exception as e:
#         print(f"数据库连接错误: {e}")
#         print("2秒后重试连接...")
#         time.sleep(2)

# def find_post(id:int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
#     post=cursor.fetchone()
#     return post
# class test(BaseModel):
#     id:int
#     title:str
#     content:str
#     published:bool
#     created_at:datetime

# class test2(BaseModel):
#     title:str
#     content:str
#     published:bool
#     created_at:datetime
#     hello:bool

# 

# @app.get("/annotation")
# def test_post(test:Annotated[test2,Depends(get_test)]):
#     print(test)
#     return {"status": "success"}



# def get_query_parameter(q: str = "dsadasd"):
#     return q 

# 使用依赖
# @app.get("/items")
# def read_items(query: str = Depends(get_query_parameter)):
#     return {"query": query}