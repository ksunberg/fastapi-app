import pytest
from hypothesis import given, strategies as st, settings
import random
from my_app.main import db

usernames = st.text(min_size=1, max_size=50)
ages = st.integers(min_value=1, max_value=150)
valid_users = st.fixed_dictionaries({
    "username": usernames,
    "age": ages
})


@pytest.mark.asyncio
@settings(max_examples=50, deadline=None,
          suppress_health_check=[settings._HypothesisHealthCheck.function_scoped_fixture])
@given(user=valid_users)
async def test_create_and_read_match(client, clear_db, user):
    create = await client.post("/users", json=user)
    assert create.status_code == 201
    created = create.json()

    get = await client.get(f"/users/{created['id']}")
    assert get.status_code == 200
    read = get.json()

    assert read["username"] == user["username"]
    assert read["age"] == user["age"]


@pytest.mark.asyncio
@settings(max_examples=30, deadline=None,
          suppress_health_check=[settings._HypothesisHealthCheck.function_scoped_fixture])
@given(users_list=st.lists(valid_users, min_size=2, max_size=5))
async def test_unique_ids(client, clear_db, users_list):
    ids = []
    for user in users_list:
        r = await client.post("/users", json=user)
        assert r.status_code == 201
        ids.append(r.json()["id"])

    assert len(ids) == len(set(ids))


@pytest.mark.asyncio
@settings(max_examples=30, deadline=None,
          suppress_health_check=[settings._HypothesisHealthCheck.function_scoped_fixture])
@given(user=valid_users)
async def test_delete_properties(client, clear_db, user):
    create = await client.post("/users", json=user)
    assert create.status_code == 201
    user_id = create.json()["id"]

    delete1 = await client.delete(f"/users/{user_id}")
    assert delete1.status_code == 204

    delete2 = await client.delete(f"/users/{user_id}")
    assert delete2.status_code == 404

    get = await client.get(f"/users/{user_id}")
    assert get.status_code == 404


@pytest.mark.asyncio
async def test_boundaries(client, clear_db):
    r = await client.post("/users", json={"username": "test", "age": 25})
    assert r.status_code == 201

    r = await client.post("/users", json={"username": "", "age": 25})
    assert r.status_code == 422

    r = await client.post("/users", json={"username": "a" * 60, "age": 25})
    assert r.status_code == 422

    r = await client.post("/users", json={"username": "test", "age": 0})
    assert r.status_code == 422

    r = await client.post("/users", json={"username": "test", "age": 200})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_stateful_operations(client, clear_db):
    oracle = {}

    for _ in range(15):
        op = random.choice(["create", "read", "delete"])

        if op == "create":
            username = f"user_{random.randint(1, 100)}"
            age = random.randint(1, 150)
            r = await client.post("/users", json={"username": username, "age": age})
            assert r.status_code == 201
            data = r.json()
            oracle[data["id"]] = {"username": username, "age": age}

        elif op == "read":
            if oracle:
                user_id = random.choice(list(oracle.keys()))
                r = await client.get(f"/users/{user_id}")
                assert r.status_code == 200
                data = r.json()
                assert data["username"] == oracle[user_id]["username"]
                assert data["age"] == oracle[user_id]["age"]
            else:
                r = await client.get(f"/users/{random.randint(1, 10)}")
                assert r.status_code == 404

        else:
            if oracle:
                user_id = random.choice(list(oracle.keys()))
                r = await client.delete(f"/users/{user_id}")
                assert r.status_code == 204
                del oracle[user_id]
            else:
                r = await client.delete(f"/users/{random.randint(1, 10)}")
                assert r.status_code == 404

        for user_id, expected in oracle.items():
            r = await client.get(f"/users/{user_id}")
            assert r.status_code == 200
            data = r.json()
            assert data["username"] == expected["username"]
            assert data["age"] == expected["age"]