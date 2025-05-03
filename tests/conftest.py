from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from app.main import app
from app.config import settings
from app.database import get_session
from app.oauth2 import create_access_token
from app import models

SQL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/api_test"

engine = create_engine(SQL_DATABASE_URL)

# def get_session_override():
#     with Session(engine, autocommit=False, autoflush=False) as session:
#         yield session

# app.dependency_overrides[get_session] = get_session_override

@pytest.fixture
def session():
    """Create a new database session for each test."""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session

@pytest.fixture
def client(session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    """Create a test user in the database."""
    user_data = {
        "email": "user1@gmail.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    """Create a test user in the database."""
    user_data = {
        "email": "user2@gmail.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    """Create a test token for the test user."""
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    """Create a test client with authorization."""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(session, test_user, test_user2):
    """Create test posts in the database."""
    post_data = [
        {
            "title": "Post 1",
            "content": "Content for post 1",
            "owner_id": test_user['id']
        },
        {
            "title": "Post 2",
            "content": "Content for post 2",
            "owner_id": test_user['id']
        },
        {
            "title": "Post 3",
            "content": "Content for post 3",
            "owner_id": test_user['id']
        },
        {
            "title": "Post 4",
            "content": "Content for post 4",
            "owner_id": test_user2['id']
        }
    ]
    session.add_all([
        models.Post(**post) for post in post_data
    ])

    session.commit()

    post = session.exec(select(models.Post)).all()
    return post