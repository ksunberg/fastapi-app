import pytest
from my_app.main import db


@pytest.mark.asyncio
async def test_create_user(client, faker, clear_db):
    user_data = {
        "username": faker.user_name(),
        "age": faker.random_int(min=18, max=99)
    }

    response = await client.post("/users", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == user_data["username"]
    assert data["age"] == user_data["age"]


@pytest.mark.asyncio
async def test_create_user_with_edge_values(client, faker, clear_db):
    user_data = {
        "username": faker.user_name()[:3],
        "age": 1
    }

    response = await client.post("/users", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["age"] == 1


@pytest.mark.asyncio
async def test_get_existing_user(client, faker, clear_db):
    user_data = {
        "username": faker.user_name(),
        "age": faker.random_int(min=18, max=99)
    }

    create_response = await client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    response = await client.get(f"/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == user_data["username"]
    assert data["age"] == user_data["age"]


@pytest.mark.asyncio
async def test_get_nonexistent_user(client, clear_db):
    response = await client.get("/users/999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_existing_user(client, faker, clear_db):
    user_data = {
        "username": faker.user_name(),
        "age": faker.random_int(min=18, max=99)
    }

    create_response = await client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    response = await client.delete(f"/users/{user_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_nonexistent_user(client, clear_db):
    response = await client.delete("/users/999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_user_twice(client, faker, clear_db):
    user_data = {
        "username": faker.user_name(),
        "age": faker.random_int(min=18, max=99)
    }

    create_response = await client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    first_delete = await client.delete(f"/users/{user_id}")
    assert first_delete.status_code == 204

    second_delete = await client.delete(f"/users/{user_id}")
    assert second_delete.status_code == 404


@pytest.mark.asyncio
async def test_multiple_users(client, faker, clear_db):
    users = []
    for _ in range(3):
        user_data = {
            "username": faker.user_name(),
            "age": faker.random_int(min=18, max=99)
        }
        response = await client.post("/users", json=user_data)
        assert response.status_code == 201
        users.append(response.json())

    assert len(users) == 3

    for user in users:
        response = await client.get(f"/users/{user['id']}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user_without_data(client, clear_db):
    response = await client.post("/users", json={})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_root_endpoint(client, clear_db):
    response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "users_count" in data
    assert data["users_count"] == len(db)