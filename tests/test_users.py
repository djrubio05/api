from app import schemas
import jwt
from app.config import settings
import pytest

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Welcome to my API, my guy!"

def test_create_user(client):
    response = client.post("/users/", json={"email": "user@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "user@gmail.com"

def test_login_user(client, test_user):
    response = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**response.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, [settings.algorithm,])
    user_id = payload.get("user_id")
    assert user_id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password", 403),
    ("user@gmail.com", "wrongpassword", 403),
    ("user@gmail.com",None, 403),
    (None, "password", 403),
    ("", "password", 403),
    ("user@gmail.com","", 403),
    ])
def test_login_user_incorrect_password(client, test_user, email, password, status_code):
    response = client.post("/login/", data={"username": email, "password": password})
    assert response.status_code == status_code