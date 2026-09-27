import pytest
from unittest.mock import AsyncMock, MagicMock
from my_app.main import app, get_db


@pytest.fixture
def mock_session():
    mock = AsyncMock()
    mock.execute = AsyncMock()
    mock.add = MagicMock()
    mock.commit = AsyncMock()
    mock.refresh = AsyncMock()
    return mock


@pytest.fixture(autouse=True)
def override_dependency(mock_session):
    async def override_get_db():
        return mock_session
    app.dependency_overrides[get_db] = override_get_db
    yield mock_session
    app.dependency_overrides.clear()
