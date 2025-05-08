from app.schema import UserResponse
from tests.database import client,session
import pytest
from app.oauth2 import get_current_user




def test_root(client):
    response = client.get("/")
    # print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "请求信息已在后端控制台打印!!!!13232dadad1QWWQEQEQWaaaaaaa"}

def test_create_user(client):
    response = client.post("/users/",json={"email":"test@test.com","password":"test"})
    # print(response.json())
    # print(response.json(),"response.json()")
    new_user = UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test@test.com"

def test_login_user(client,test_user):

    response = client.post("/auth/login/",data={"username":test_user["email"],"password":test_user["password"]})
    # print(response.json(),"response.json()")
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert client.get(f"/users/{test_user['id']}").json()["id"] == test_user["id"]
    # 获取token
@pytest.mark.parametrize("email,password,status_code",[
    ("wrong@test.com","test",403),
    ("test@test.com","wrong_password",403),
    ("wrong@test.com","wrong_password",403),
    (None,"test",403),
    ("test@test.com",None,403),
])
def test_incorrect_login(client,test_user,email,password,status_code):
    response =client.post("/auth/login/",data={"username":email,"password":password})
    print(response.json(),"response.json()")
    assert response.status_code == status_code
    


# test_root()
