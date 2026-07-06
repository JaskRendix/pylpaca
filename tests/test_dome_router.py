import httpx
import pytest
from fastapi import FastAPI

from services.config import ascom_config
from services.dome_router import get_dome_router


@pytest.fixture
def app(dome_driver):
    app = FastAPI()
    app.include_router(get_dome_router(0), prefix="/api/v1/dome/0")
    return app


@pytest.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_invalid_device_number(client):
    r = await client.get("/api/v1/dome/99/shutterstatus")
    assert r.status_code in (404, 500)


@pytest.mark.asyncio
async def test_invalid_route(client):
    r = await client.get("/api/v1/dome/0/doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_missing_driver_instance(client):
    key = ("dome", 0)
    saved = ascom_config._drivers.pop(key)
    r = await client.get("/api/v1/dome/0/shutterstatus")
    assert r.status_code == 500
    ascom_config._drivers[key] = saved


@pytest.mark.asyncio
async def test_invalid_bool_query_param(client):
    r = await client.put("/api/v1/dome/0/connected?Connected=notabool")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_driver_method_raises_exception(client, monkeypatch, dome_driver):
    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(dome_driver, "OpenShutter", boom)
    r = await client.put("/api/v1/dome/0/openshutter")
    assert r.status_code == 500


@pytest.mark.asyncio
async def test_wrong_http_method(client):
    r = await client.post("/api/v1/dome/0/shutterstatus")
    assert r.status_code == 405


@pytest.mark.asyncio
async def test_invalid_query_param_name(client):
    r = await client.put("/api/v1/dome/0/connected?WrongParam=true")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_invalid_enum_value(client):
    r = await client.put("/api/v1/dome/0/openshutter?State=999")
    assert r.status_code in (200, 422)


@pytest.mark.asyncio
async def test_missing_required_query_param(client):
    r = await client.put("/api/v1/dome/0/connected")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_invalid_json_body(client):
    r = await client.put(
        "/api/v1/dome/0/openshutter",
        content="not-json",
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 200
