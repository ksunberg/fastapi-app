import time

import pytest
from my_app.main import SESSION_COOKIE, signer


def test_login_success_sets_cookie(client, credentials):
    r = client.post("/login", data=credentials)
    assert r.status_code == 200
    assert r.json() == {"message": "Login successful"}
    assert SESSION_COOKIE in r.cookies


def test_login_wrong_password(client):
    r = client.post("/login", data={"username": "ksu", "password": "wrong"})
    assert r.status_code == 401
    assert r.json() == {"message": "Invalid credentials"}
    assert SESSION_COOKIE not in r.cookies


def test_login_unknown_user(client):
    r = client.post("/login", data={"username": "nobody", "password": "123"})
    assert r.status_code == 401
    assert r.json() == {"message": "Invalid credentials"}


def test_login_missing_fields(client):
    r = client.post("/login", data={"username": "ksu"})
    assert r.status_code == 422


def test_profile_no_cookie(client):
    r = client.get("/profile")
    assert r.status_code == 401
    assert r.json() == {"message": "Invalid session"}


def test_profile_valid_cookie(client, logged_in_cookie):
    r = client.get("/profile", cookies={SESSION_COOKIE: logged_in_cookie})
    assert r.status_code == 200
    body = r.json()
    assert body["message"] == "Profile data"
    expected_user_id = signer.unsign(logged_in_cookie).decode()
    assert body["user_id"] == expected_user_id


def test_profile_tampered_cookie(client):
    r = client.get("/profile", cookies={SESSION_COOKIE: "garbage.value"})
    assert r.status_code == 401
    assert r.json() == {"message": "Invalid session"}


def test_profile_cookie_signed_with_other_key(client, make_signed_cookie):
    bad = make_signed_cookie(secret="another-key")
    r = client.get("/profile", cookies={SESSION_COOKIE: bad})
    assert r.status_code == 401
    assert r.json() == {"message": "Invalid session"}


def test_profile_expired_session(client, logged_in_cookie, freeze_ttl):
    freeze_ttl(ttl=-1, renew=-1)
    r = client.get("/profile", cookies={SESSION_COOKIE: logged_in_cookie})
    assert r.status_code == 401
    assert r.json() == {"message": "Session expired"}


def test_profile_renews_when_past_threshold(client, logged_in_cookie, monkeypatch):
    import my_app.main as app_module
    real_time = time.time
    monkeypatch.setattr(
        app_module.signer, "get_timestamp", lambda: int(real_time()) + 200
    )
    r = client.get("/profile", cookies={SESSION_COOKIE: logged_in_cookie})
    assert r.status_code == 200
    assert r.json()["message"] == "Profile data"
    new_cookie = r.cookies.get(SESSION_COOKIE)
    assert new_cookie is not None
    assert new_cookie != logged_in_cookie


def test_profile_no_renew_within_threshold(client, logged_in_cookie):
    r = client.get("/profile", cookies={SESSION_COOKIE: logged_in_cookie})
    assert r.status_code == 200
    assert r.cookies.get(SESSION_COOKIE) is None