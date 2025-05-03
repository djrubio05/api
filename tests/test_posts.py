import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    posts = response.json()

    posts_list = [schemas.PostVote(**post) for post in posts]
    assert len(posts_list) == len(test_posts)
    assert response.status_code == 200
    assert posts_list[0].Post.title == test_posts[0].title
    assert posts_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_found(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/9999999999")
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVote(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("Updated Title", "Updated Content", True),
    ("Another Title", "Another Content", False),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    created_post = schemas.PostOut(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published(authorized_client, test_user):
    response = authorized_client.post("/posts/", json={
        "title": "New Post",
        "content": "New Content"
    })
    created_post = schemas.PostOut(**response.json())
    assert response.status_code == 201
    assert created_post.title == "New Post"
    assert created_post.content == "New Content"
    assert created_post.published == True  # Default value should be True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_posts):
    response = client.post("/posts/", json={
        "title": "New Post",
        "content": "New Content"
    })
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

    get_response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert get_response.status_code == 404

def test_delete_post_not_found(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/9999999999")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": False
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.published == data['published']

def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": False
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403

def test_update_post_not_found(authorized_client, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": False
    }
    response = authorized_client.put(f"/posts/9999999999", json=data)
    assert response.status_code == 404
    
def test_unauthorized_user_update_post(client, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": False
    }
    response = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert response.status_code == 401

    