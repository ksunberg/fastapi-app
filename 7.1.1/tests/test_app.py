import pytest
from fastapi.testclient import TestClient
from my_app.main import app
from unittest.mock import MagicMock

client = TestClient(app)


def test_register_success(mock_session, override_dependency):
    payload = {"username": "kot", "password": "ghpH1845"}
    response = client.post("/register", json=payload)
    assert response.status_code == 200
    assert response.json() == {"massage": "Пользователь создан"}
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_user_info_found(mock_session, override_dependency):
    user_id = 1
    fake_user = MagicMock()
    fake_user.id = user_id
    fake_user.username = "kot"
    fake_user.password = "password"
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_user
    mock_session.execute.return_value = result_mock
    response = client.get(f"/user_info/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "kot"


def test_user_info_not_found(mock_session, override_dependency):
    user_id = 999
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = result_mock
    response = client.get(f"/user_info/{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Пользователь не найден"


def test_get_all_users(mock_session, override_dependency):
    user1 = MagicMock()
    user1.id = 1
    user1.username = "kot"
    user1.password = "password1"
    user2 = MagicMock()
    user2.id = 2
    user2.username = "kotik"
    user2.password = "password2"
    users_list = [user1, user2]
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = users_list
    mock_session.execute.return_value = result_mock
    response = client.get("/all_user_info")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["username"] == "kot"
    assert data[0]["password"] == "password1"
    assert data[1]["id"] == 2
    assert data[1]["username"] == "kotik"
    assert data[1]["password"] == "password2"

