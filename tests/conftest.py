from fastapi.testclient import TestClient
from my_app.pytest1 import app
import pytest
from unittest.mock import AsyncMock, Mock
from my_app.pytest1 import app, get_db

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db():
    session = AsyncMock()
    result = Mock()
    result.scalar_one_or_none = Mock(return_value=None)
    session.execute = AsyncMock(return_value=result)
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    return session

@pytest.fixture
def override_db(mock_db):
    async def _get_db():
        yield mock_db
    app.dependency_overrides[get_db] = _get_db
    yield mock_db
    app.dependency_overrides.clear()