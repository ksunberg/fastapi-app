from unittest.mock import Mock


def test_create_user(client, override_db):
    r = client.post("/users/", json={"username": "john", "password": "123456"})
    assert r.status_code == 200
    assert r.json() == {"message": "OK"}


def test_create_duplicate(client, override_db):
    result = Mock()
    result.scalar_one_or_none = Mock(return_value=Mock())
    override_db.execute.return_value = result
    r = client.post("/users/", json={"username": "john", "password": "123456"})
    assert r.status_code == 400


def test_get_user(client, override_db):
    user = Mock(id=1, username="john", password="123456")
    result = Mock()
    result.scalar_one_or_none = Mock(return_value=user)
    override_db.execute.return_value = result
    r = client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["username"] == "john"


def test_get_user_not_found(client, override_db):
    r = client.get("/users/999")
    assert r.status_code == 404


def test_delete_user(client, override_db):
    user = Mock()
    result = Mock()
    result.scalar_one_or_none = Mock(return_value=user)
    override_db.execute.return_value = result
    r = client.delete("/users/1")
    assert r.status_code == 200
    assert r.json() == {"message": "OK"}


def test_delete_not_found(client, override_db):
    r = client.delete("/users/999")
    assert r.status_code == 404