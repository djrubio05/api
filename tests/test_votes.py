import pytest
from app import models

@pytest.fixture
def test_vote(test_posts, session, test_user):
    """Create a test vote in the database."""
    vote_data = {
        "post_id": test_posts[3].id,
        "user_id": test_user['id']
    }
    session.add(models.Vote(**vote_data))
    session.commit()
    return vote_data

def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(f"/vote/", json={"post_id": test_posts[3].id, "direction": 1})
    assert response.status_code == 201

def test_vote_twice_on_post(authorized_client, test_vote):
    response = authorized_client.post(f"/vote/", json={"post_id": test_vote['post_id'], "direction": 1})
    assert response.status_code == 409

def test_delete_vote(authorized_client, test_vote):
    response = authorized_client.post(f"/vote/", json={"post_id": test_vote['post_id'], "direction": 0})
    assert response.status_code == 201

def test_delete_vote_not_exist(authorized_client, test_posts):
    response = authorized_client.post(f"/vote/", json={"post_id": test_posts[0].id, "direction": 0})
    assert response.status_code == 404

def test_vote_on_post_not_exist(authorized_client):
    response = authorized_client.post(f"/vote/", json={"post_id": 9999999999, "direction": 1})
    assert response.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    response = client.post(f"/vote/", json={"post_id": test_posts[3].id, "direction": 1})
    assert response.status_code == 401