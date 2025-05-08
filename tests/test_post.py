from app.schema import post_vote_Response
import pytest

def test_get_all_posts(authorized_client,test_posts):
    response = authorized_client.get("/posts/")
    print(response.json(),"test_get_all_posts response.json()")
    def validate(post):
        return post_vote_Response(**post)
    posts = list(map(validate,response.json()))
    print(posts,"posts from test_get_all_posts")
    assert len(posts) == len(test_posts)
    assert response.status_code == 200
    assert posts[0].Post.id == test_posts[0].id
    assert posts[0].Post.title == test_posts[0].title
    assert posts[0].Post.content == test_posts[0].content
    # assert posts[0].Post.owner_id == test_posts[0].owner_id
    # assert posts[0].Post.created_at == test_posts[0].created_at
    # assert posts[0].Post.updated_at == test_posts[0].updated_at
    # assert posts[0].Post.owner.id == test_posts[0].owner.id
    # assert posts[0].Post.owner.email == test_posts[0].owner.email
    # assert posts[0].Post.owner.password == test_posts[0].owner.password

def test_unauthorized_user_get_all_posts(client,test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_get_one_post(client,test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    print(response.json(),"test_get_one_post response.json()")
    assert response.status_code == 200
    assert response.json().get("Post").get("id") == test_posts[0].id
    assert response.json().get("Post").get("title") == test_posts[0].title
    assert response.json().get("Post").get("content") == test_posts[0].content

def test_unauthorized_user_get_one_post(client,test_posts):
    response = client.get(f"/posts/9999")
    assert response.status_code == 404



@pytest.mark.parametrize("id,title,content,published",[
    (1,"first title","first content",True),
    (2,"second title","second content",False),
    (3,"third title","third content",True),
])
def test_create_post(authorized_client,test_user,id,title,content,published):
    response = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    print(response.json(),"response.json()")
    assert response.status_code == 201
    assert response.json().get("title") == title
    assert response.json().get("content") == content
    assert response.json().get("published") == published
    assert response.json().get("owner_id") == test_user.get("id")


def test_unauthorized_user_create_post(client,test_user):
    response = client.post("/posts/",json={"title":"test title","content":"test content"})
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_post(authorized_client,test_user,test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_non_exist(authorized_client,test_user,test_posts):
    response = authorized_client.delete(f"/posts/9999")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,test_user1,test_posts):
    print(test_posts[3].id,"test_posts[3].id")
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    print(response.json(),"response.json()")
    assert response.status_code == 403


def test_update_post(authorized_client,test_user,test_posts):
    data={"title":"updated title","content":"updated content","id":test_posts[0].id}
    response = authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    assert response.status_code == 200
    assert response.json().get("title") == data.get("title")
    assert response.json().get("content") == data.get("content")

def test_create_post_default_published_true(authorized_client,test_user):
    response = authorized_client.post("/posts/",json={"title":"test title","content":"test content"})
    print(response.json(),"response.json()")
    assert response.status_code == 201
    assert response.json().get("published") == False
    assert response.json().get("owner_id") == test_user.get("id")
    assert response.json().get("title") == "test title"
    assert response.json().get("content") == "test content"



# def test_unauthorized_user_get_all_posts(client):
#     response = client.get("/posts/")
#     assert response.status_code == 401
