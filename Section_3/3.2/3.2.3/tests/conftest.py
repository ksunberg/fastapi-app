import pytest
from fastapi.testclient import TestClient

import my_app.main as app_module
from my_app.main import app, signer, SESSION_COOKIE


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def credentials():
    username = next(iter(app_module.fake_bd))
    return {"username": username, "password": app_module.fake_bd[username]}


@pytest.fixture
def logged_in_cookie(client, credentials):
    r = client.post("/login", data=credentials)
    assert r.status_code == 200
    return r.cookies[SESSION_COOKIE]


@pytest.fixture
def make_signed_cookie():
    from itsdangerous import TimestampSigner
    def _make(value: str = "user-1", secret: str | None = None):
        return TimestampSigner(secret or app_module.SECRET_KEY).sign(value).decode()
    return _make


@pytest.fixture
def freeze_ttl(monkeypatch):
    def _freeze(ttl: int = None, renew: int = None):
        if ttl is not None:
            monkeypatch.setattr(app_module, "SESSION_TTL", ttl)
        if renew is not None:
            monkeypatch.setattr(app_module, "RENEW_THRESHOLD", renew)
    return _freeze
