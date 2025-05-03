from hmac import new
from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, create_engine, SQLModel
from app.main import app
from app.config import settings
from app.database import get_session

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
        "email": "user@gmail.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user