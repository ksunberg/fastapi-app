import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from my_app.main import app, db

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def faker():
    from faker import Faker
    return Faker()

@pytest.fixture
def clear_db():
    db.clear()
    yield
    db.clear()