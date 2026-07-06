import httpx
import pytest
from fastapi import FastAPI

from ASCOMDriver.DeviceInterfaces.Enumerations import ShutterState
from services.device_router import make_device_router


@pytest.fixture
def app(dome_driver):
    resources = {
        "shutterstatus": "ShutterStatus",
        "openshutter": "OpenShutter",
        "closeshutter": "CloseShutter",
    }
    router = make_device_router("dome", 0, resources)
    app = FastAPI()
    app.include_router(router, prefix="/api/v1/dome/0")
    return app


@pytest.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, expected",
    [
        ("/api/v1/dome/0/shutterstatus", ShutterState.shutterClosed),
        ("/api/v1/dome/0/connected", False),
    ],
)
async def test_dome_get_endpoints(client, dome_driver, endpoint, expected):
    r = await client.get(endpoint)
    assert r.status_code == 200
    assert r.json()["ErrorNumber"] == 0
    assert r.json()["Value"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, attr, expected",
    [
        ("/api/v1/dome/0/openshutter", "ShutterStatus", ShutterState.shutterOpen),
        ("/api/v1/dome/0/closeshutter", "ShutterStatus", ShutterState.shutterClosed),
    ],
)
async def test_dome_put_endpoints(client, dome_driver, endpoint, attr, expected):
    r = await client.put(endpoint)
    assert r.status_code == 200
    assert getattr(dome_driver, attr) == expected


@pytest.mark.asyncio
async def test_connected_set_and_get(client, dome_driver):
    r = await client.put("/api/v1/dome/0/connected?Connected=true")
    assert r.status_code == 200
    assert dome_driver.Connected is True
    r = await client.get("/api/v1/dome/0/connected")
    assert r.status_code == 200
    assert r.json()["Value"] is True


@pytest.mark.asyncio
async def test_unknown_resource_404(client):
    r = await client.get("/api/v1/dome/0/doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_driver_exception_500(client, dome_driver, monkeypatch):
    monkeypatch.setattr(
        type(dome_driver),
        "ShutterStatus",
        property(lambda self: (_ for _ in ()).throw(RuntimeError("boom"))),
    )
    r = await client.get("/api/v1/dome/0/shutterstatus")
    assert r.status_code == 500


@pytest.mark.asyncio
async def test_wrong_device_number(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/api/v1/dome/99/shutterstatus")
        assert r.status_code == 404


@pytest.mark.asyncio
async def test_wrong_device_type(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/api/v1/telescope/0/shutterstatus")
        assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint",
    [
        "/api/v1/dome/0/shutterstatus",
        "/api/v1/dome/0/connected",
    ],
)
async def test_json_envelope(client, endpoint):
    r = await client.get(endpoint)
    body = r.json()
    assert "ClientTransactionID" in body
    assert "ServerTransactionID" in body
    assert "ErrorNumber" in body
    assert "ErrorMessage" in body
    assert "Value" in body


@pytest.mark.asyncio
async def test_router_calls_correct_driver_attribute(client, dome_driver, monkeypatch):
    called = {}

    def fake_open(self):
        called["open"] = True

    monkeypatch.setattr(type(dome_driver), "OpenShutter", fake_open)
    await client.put("/api/v1/dome/0/openshutter")
    assert called.get("open") is True


@pytest.mark.asyncio
async def test_callable_vs_attribute(dome_driver, monkeypatch):
    setattr(type(dome_driver), "Foo", lambda self: 123)
    resources = {
        "shutterstatus": "Foo",
        "openshutter": "OpenShutter",
        "closeshutter": "CloseShutter",
    }
    app = FastAPI()
    router = make_device_router("dome", 0, resources)
    app.include_router(router, prefix="/api/v1/dome/0")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/api/v1/dome/0/shutterstatus")
        assert r.status_code == 200
        assert r.json()["Value"] == 123
