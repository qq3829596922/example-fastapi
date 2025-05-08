from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base,Post
import pytest
from app.oauth2 import create_access_token
sqlalchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(sqlalchemy_database_url)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    print("清除所有table")
    Base.metadata.create_all(bind=engine)

    session = TestSessionLocal()
    print("session已被创建")
    try:
        yield session
    finally:
        session.close()
# 创建表函数

    # 导入模型以确保它们被映射到Base

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session   
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"email":"test@test.com","password":"test"}
    response = client.post("/users/",json=user_data)
    # print(response.json())
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"]=user_data["password"]
    # print(new_user,"new_user from test_user")
    return new_user

@pytest.fixture()
def test_user1(client):
    user_data = {"email":"test1@test.com","password":"test"}
    response = client.post("/users/",json=user_data)
    # print(response.json())
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"]=user_data["password"]
    # print(new_user,"new_user from test_user")
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})

@pytest.fixture()
def authorized_client(client,token):
    # print(token,"token")
    client.headers.update({"Authorization":f"Bearer {token}"})
    return client

@pytest.fixture()
def test_posts(test_user,test_user1,session):
    post=[{
        "title":"first title",
        "content":"first content",
        "owner_id":test_user["id"]
    },
    {
        "title":"second title",
        "content":"second content",
        "owner_id":test_user["id"]
    },
    {
        "title":"third title",
        "content":"third content",
        "owner_id":test_user["id"]
    },
    {
        "title":"fourth title",
        "content":"fourth content",
        "owner_id":test_user1["id"]
    }
    ]
    def create_post_model(post):
        return Post(**post)
    post_map = map(create_post_model,post)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(Post).all()
    return posts


# def test_fixture(client):
#     client
#     pass