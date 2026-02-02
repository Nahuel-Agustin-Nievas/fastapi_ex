from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.main import app

from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# TestClient(
#     app,
#     base_url="http://testserver",
#     raise_server_exceptions=True,
#     root_path="",
#     backend="asyncio",
#     backend_options=None,
#     cookies=None,
#     headers=None,
#     follow_redirects=True,
#     client=("testclient", 50000),
# )

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost:5432/fastapi_test_db'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# client = TestClient(app)


@pytest.fixture(scope="function")
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)
    

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user
   

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        # **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@example.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    },
    {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user2["id"]
    }]

    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()
    posts = session.query(models.Post).all()
    return posts


