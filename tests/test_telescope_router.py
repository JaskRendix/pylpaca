import pytest
import httpx
from fastapi import FastAPI

from services.config import ascom_config
from services.telescope_router import get_telescope_router


class MockTelescopeDriver:
    def __init__(self):
        self.Connected = False
        self._connecting = False
        self._device_state = []
        self._ra = 1.23
        self._dec = -4.56
        self._tracking = False
        self._tracking_rate = 0
        self._slewing = False
        self._utcdate = 123456.0
        self._sidereal = 12.34

    def Connect(self):
        self._connecting = True
        self.Connected = True
        self._connecting = False
        return True

    def Disconnect(self):
        self._connecting = True
        self.Connected = False
        self._connecting = False
        return True

    @property
    def Connecting(self):
        return self._connecting

    @property
    def DeviceState(self):
        return self._device_state

    def AbortSlew(self):
        return True

    @property
    def RightAscension(self):
        return self._ra

    @property
    def Declination(self):
        return self._dec

    @property
    def SiderealTime(self):
        return self._sidereal

    @property
    def UTCDate(self):
        return self._utcdate

    @property
    def Slewing(self):
        return self._slewing

    @property
    def Tracking(self):
        return self._tracking

    @Tracking.setter
    def Tracking(self, value):
        self._tracking = value

    @property
    def TrackingRate(self):
        return self._tracking_rate

    @TrackingRate.setter
    def TrackingRate(self, value):
        self._tracking_rate = value

    def SlewToCoordinates(self, ra, dec):
        self._ra = ra
        self._dec = dec
        return True


@pytest.fixture
def app():
    ascom_config.set_driver_instance("telescope", 0, MockTelescopeDriver())
    app = FastAPI()
    app.include_router(get_telescope_router(0), prefix="/api/v1/telescope/0")
    return app


@pytest.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_rightascension(client):
    r = await client.get("/api/v1/telescope/0/rightascension")
    assert r.status_code == 200
    assert r.json()["Value"] == 1.23


@pytest.mark.asyncio
async def test_declination(client):
    r = await client.get("/api/v1/telescope/0/declination")
    assert r.status_code == 200
    assert r.json()["Value"] == -4.56


@pytest.mark.asyncio
async def test_siderealtime(client):
    r = await client.get("/api/v1/telescope/0/siderealtime")
    assert r.status_code == 200
    assert r.json()["Value"] == 12.34


@pytest.mark.asyncio
async def test_utcdate(client):
    r = await client.get("/api/v1/telescope/0/utcdate")
    assert r.status_code == 200
    assert r.json()["Value"] == 123456.0


@pytest.mark.asyncio
async def test_slewing(client):
    r = await client.get("/api/v1/telescope/0/slewing")
    assert r.status_code == 200
    assert r.json()["Value"] is False


@pytest.mark.asyncio
async def test_get_tracking(client):
    r = await client.get("/api/v1/telescope/0/tracking")
    assert r.status_code == 200
    assert r.json()["Value"] is False


@pytest.mark.asyncio
async def test_set_tracking(client):
    r = await client.put("/api/v1/telescope/0/tracking?Tracking=true")
    assert r.status_code == 200
    assert r.json()["Value"] is True

    r2 = await client.get("/api/v1/telescope/0/tracking")
    assert r2.json()["Value"] is True


@pytest.mark.asyncio
async def test_get_tracking_rate(client):
    r = await client.get("/api/v1/telescope/0/trackingrate")
    assert r.status_code == 200
    assert r.json()["Value"] == 0


@pytest.mark.asyncio
async def test_set_tracking_rate(client):
    r = await client.put("/api/v1/telescope/0/trackingrate?TrackingRate=2")
    assert r.status_code == 200
    assert r.json()["Value"] == 2

    r2 = await client.get("/api/v1/telescope/0/trackingrate")
    assert r2.json()["Value"] == 2


@pytest.mark.asyncio
async def test_slewtocoordinates(client):
    r = await client.put("/api/v1/telescope/0/slewtocoordinates?RightAscension=5.5&Declination=-1.2")
    assert r.status_code == 200
    assert r.json()["Value"] is True

    r2 = await client.get("/api/v1/telescope/0/rightascension")
    assert r2.json()["Value"] == 5.5

    r3 = await client.get("/api/v1/telescope/0/declination")
    assert r3.json()["Value"] == -1.2


@pytest.mark.asyncio
async def test_abortslew(client):
    r = await client.put("/api/v1/telescope/0/abortslew")
    assert r.status_code == 200
    assert r.json()["Value"] is True


@pytest.mark.asyncio
async def test_connect(client):
    r = await client.put("/api/v1/telescope/0/connect")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/telescope/0/connected")
    assert r2.json()["Value"] is True


@pytest.mark.asyncio
async def test_disconnect(client):
    await client.put("/api/v1/telescope/0/connect")

    r = await client.put("/api/v1/telescope/0/disconnect")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/telescope/0/connected")
    assert r2.json()["Value"] is False


@pytest.mark.asyncio
async def test_connecting_flag(client):
    r = await client.get("/api/v1/telescope/0/connecting")
    assert r.status_code == 200
    assert r.json()["Value"] is False


@pytest.mark.asyncio
async def test_devicestate(client):
    r = await client.get("/api/v1/telescope/0/devicestate")
    assert r.status_code == 200
    assert r.json()["Value"] == []


@pytest.mark.asyncio
async def test_invalid_route(client):
    r = await client.get("/api/v1/telescope/0/doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_wrong_http_method(client):
    r = await client.post("/api/v1/telescope/0/rightascension")
    assert r.status_code == 405


@pytest.mark.asyncio
async def test_missing_driver_instance(client):
    key = ("telescope", 0)
    saved = ascom_config._drivers.pop(key)

    r = await client.get("/api/v1/telescope/0/rightascension")
    assert r.status_code == 500

    ascom_config._drivers[key] = saved


@pytest.mark.asyncio
async def test_invalid_bool_query_param(client):
    r = await client.put("/api/v1/telescope/0/tracking?Tracking=notabool")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_invalid_int_query_param(client):
    r = await client.put("/api/v1/telescope/0/trackingrate?TrackingRate=notanint")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_missing_required_query_param(client):
    r = await client.put("/api/v1/telescope/0/slewtocoordinates")
    assert r.status_code == 422
