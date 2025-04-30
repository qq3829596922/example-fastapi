from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from app.config import settings

sqlalchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(sqlalchemy_database_url)

try:
    engine = create_engine(sqlalchemy_database_url)
    # 尝试连接

    with engine.connect() as connection:
        print(" 数据库连接成功!")
except sqlalchemy.exc.OperationalError as e:
    print(f"数据库连接失败: {e}")

# 创建声明性基类
Base = declarative_base()
print("导入前Base.metadata.tables:", len(Base.metadata.tables))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    
    db = SessionLocal()
    print("from_get_db:数据库连接成功!")
    try:
        print("from_get_db:获取数据库连接!")
        yield db
    finally:
        db.close()
        print("from_get_db:数据库连接关闭!")

# 创建表函数
def create_tables():
    # 导入模型以确保它们被映射到Base
    
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功!")

