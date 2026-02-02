
import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    print(response.json())
    assert response.status_code == 200
    posts = [schemas.PostOut(**post) for post in response.json()]
    print(posts)
    assert len(posts) == len(test_posts)
    # assert posts[0].Post.id == test_posts[0].id
    # assert len(response.json()) == len(test_posts)
    

def test_unauthorized_user_get_all_posts(client):
    response = client.get("/posts/")
    print(response.json())
    assert response.status_code == 401  # Unauthorized


    
def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401  # Unauthorized

def test_get_one_post_not_exists(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/9999")
    assert response.status_code == 404  # Not Found

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(response.json())
    post = schemas.PostOut(**response.json())
    print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert response.status_code == 200



@pytest.mark.parametrize("title, content, published", [
    ("Test Post 1", "Content for test post 1", True),
    ("Test Post 2", "Content for test post 2", False),
    ("Test Post 3", "Content for test post 3", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    created_post = schemas.Post(**response.json())
    assert created_post.title == title
    assert created_post.content == content
    print(created_post.content)
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]
    assert response.status_code == 201

def test_create_post_default_published(authorized_client, test_user):
    response = authorized_client.post("/posts/", json={
        "title": "Test Post Default Published",
        "content": "Content for test post default published"
    })
    created_post = schemas.Post(**response.json())
    assert created_post.title == "Test Post Default Published"
    assert created_post.content == "Content for test post default published"
    print(created_post.published)
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]
    assert response.status_code == 201


def test_unauthorized_user_create_post(client):
    response = client.post("/posts/", json={
        "title": "Unauthorized Post",
        "content": "Content for unauthorized post"
    })
    assert response.status_code == 401  # Unauthorized

def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    print(response.json())
    print(test_posts[0].id)
    assert response.status_code == 401  # Unauthorized


def test_delete_post_success(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204  # No Content


def test_delete_post_not_found(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/9999")
    assert response.status_code == 404  # Not Found

def test_delete_post_not_owner(authorized_client, test_posts, test_user):
    # Create a new user
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403  # Forbidden

def test_update_post(authorized_client, test_posts, test_user):
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={
            "title": "Updated Title",
            "content": "Updated Content",
            "published": False
        }
    )
    updated_post = schemas.Post(**response.json())
    assert updated_post.title == "Updated Title"
    assert updated_post.content == "Updated Content"
    assert updated_post.published == False
    assert response.status_code == 200


def test_another_user_update_post(authorized_client,client, test_posts):
    response = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json={
            "title": "Hacked Title",
            "content": "Hacked Content",
            "published": True
        }
    )
    assert response.status_code == 403  # Unauthorized

def test_unauthorized_user_update_post(client, test_posts):
    response = client.put(
        f"/posts/{test_posts[0].id}",
        json={
            "title": "Unauthorized Update",
            "content": "Unauthorized Content",
            "published": True
        }
    )
    assert response.status_code == 401  # Unauthorized


def test_update_post_not_found(authorized_client, test_posts):
    response = authorized_client.put(
        f"/posts/9999",
        json={
            "title": "Non-existent Update",
            "content": "Non-existent Content",
            "published": True
        }
    )
    assert response.status_code == 404  # Not Found
