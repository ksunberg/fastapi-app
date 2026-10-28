class TestUserApi:
    """Асинхронные тесты трёх эндпоинтов через httpx.AsyncClient + ASGITransport."""

    async def test_create_user_and_validate_response(self, client, faker):
        payload = {
            "username": faker.user_name(),
            "age": faker.random_int(min=18, max=99),
        }
        response = await client.post("/users", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] >= 1
        assert data["username"] == payload["username"]
        assert data["age"] == payload["age"]

    async def test_create_user_with_boundary_age_and_check_saved(self, client, faker):
        payload = {
            "username": faker.user_name()[:3],
            "age": 1,
        }
        response = await client.post("/users", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["age"] == 1

        get_response = await client.get(f"/users/{data['id']}")
        assert get_response.status_code == 200
        assert get_response.json() == data

    async def test_get_existing_user(self, client, faker):
        payload = {
            "username": faker.user_name(),
            "age": faker.random_int(min=18, max=99),
        }
        create_response = await client.post("/users", json=payload)
        user_id = create_response.json()["id"]

        response = await client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == payload["username"]
        assert data["age"] == payload["age"]

    async def test_get_nonexistent_user(self, client):
        response = await client.get("/users/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    async def test_delete_existing_user(self, client, faker):
        payload = {
            "username": faker.user_name(),
            "age": faker.random_int(min=18, max=99),
        }
        create_response = await client.post("/users", json=payload)
        user_id = create_response.json()["id"]

        response = await client.delete(f"/users/{user_id}")

        assert response.status_code == 204

        get_response = await client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    async def test_delete_nonexistent_user(self, client):
        response = await client.delete("/users/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    async def test_delete_user_twice(self, client, faker):
        payload = {
            "username": faker.user_name(),
            "age": faker.random_int(min=18, max=99),
        }
        create_response = await client.post("/users", json=payload)
        user_id = create_response.json()["id"]

        first_delete = await client.delete(f"/users/{user_id}")
        assert first_delete.status_code == 204

        second_delete = await client.delete(f"/users/{user_id}")
        assert second_delete.status_code == 404

    async def test_create_user_without_data_returns_422(self, client):
        response = await client.post("/users", json={})

        assert response.status_code == 422
