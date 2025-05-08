
def test_vote_post(authorized_client,test_user,test_posts):

    response = authorized_client.post("/vote/",json={"post_id":test_posts[0].id,"dir":1})


    print(response.json(),"response.json()")
    
    assert response.status_code == 201

def test_vote_post_twice(authorized_client,test_user,test_posts):
    post_id=test_posts[0].id    
    response = authorized_client.post("/vote/",json={"post_id":post_id,"dir":1})
    assert response.status_code == 201
    response = authorized_client.post("/vote/",json={"post_id":post_id,"dir":1})
    assert response.status_code == 409

# def test_unauthorized_user_vote_post(client,test_posts):
#     response = client.post("/votes/",json={"post_id":test_posts[0].id,"dir":1})
#     assert response.status_code == 401



