import pytest
from app.main import get_application
from httpx import AsyncClient
from mongomock_motor import AsyncMongoMockClient
from data.database import get_database

app = get_application()

def get_fake_database():
    return AsyncMongoMockClient()["whatsapp"]

app.dependency_overrides[get_database] = get_fake_database





@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()
