import pytest
from httpx import ASGITransport, AsyncClient

from pylpaca.server import app, register_services
from services.config import ascom_config


@pytest.fixture(scope="session", autouse=True)
def setup_app():
    register_services()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def dome_driver():
    return ascom_config.get_driver_instance("dome", 0)
