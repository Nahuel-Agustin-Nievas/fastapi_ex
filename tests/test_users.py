import pytest
from jose import jwt
from app import models, schemas
# from .database import client, session
from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     # assert response.status_code == 200
#     # assert response.json() == {"message": "Hello, World!"}
#     print(response.json().get("message"))
#     assert response.json() == {"message": "Hello World!"}
#     assert response.status_code == 200




def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"})
    
    new_user = schemas.UserOut(**response.json())
    print(response.json())
    # print(vars(response))
    assert new_user.email == "test@example.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "password123"})
    print(response.json())
    assert response.status_code == 200

def test_login2(client, test_user):
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("incorrect@example.com", "incorrectpassword", 403),
    ("test@example.com", "incorrectpassword", 403),
    ("incorrect@example.com", "password123", 403),
    (None, "password123", 422),
    ("test@example.com", None, 422)

])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login",
        data={"username": email, "password": password   })
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid Credentials" 