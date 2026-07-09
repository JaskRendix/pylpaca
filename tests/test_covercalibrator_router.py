import httpx
import pytest
from fastapi import FastAPI

from services.config import ascom_config
from services.covercalibrator_router import get_covercalibrator_router


class MockCoverCalibratorDriver:
    def __init__(self):
        self.Connected = False
        self._connecting = False
        self._cover_state = 0
        self._cal_state = 0
        self._brightness = 0
        self._max_brightness = 100

    # V2 connection workflow
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

    # Cover operations
    @property
    def CoverState(self):
        return self._cover_state

    def OpenCover(self):
        self._cover_state = 1
        return True

    def CloseCover(self):
        self._cover_state = 2
        return True

    def HaltCover(self):
        self._cover_state = 3
        return True

    # Calibrator operations
    @property
    def CalibratorState(self):
        return self._cal_state

    @property
    def Brightness(self):
        return self._brightness

    @property
    def MaxBrightness(self):
        return self._max_brightness

    def CalibratorOn(self, Brightness: int):
        self._brightness = Brightness
        self._cal_state = 1
        return True

    def CalibratorOff(self):
        self._brightness = 0
        self._cal_state = 0
        return True


@pytest.fixture
def app():
    ascom_config.set_driver_instance("covercalibrator", 0, MockCoverCalibratorDriver())
    app = FastAPI()
    app.include_router(
        get_covercalibrator_router(0), prefix="/api/v1/covercalibrator/0"
    )
    return app


@pytest.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_connected(client):
    r = await client.get("/api/v1/covercalibrator/0/connected")
    assert r.status_code == 200
    assert r.json()["Value"] is False


@pytest.mark.asyncio
async def test_set_connected(client):
    r = await client.put("/api/v1/covercalibrator/0/connected?Connected=true")
    assert r.status_code == 200
    assert r.json()["Value"] is True

    r2 = await client.get("/api/v1/covercalibrator/0/connected")
    assert r2.json()["Value"] is True


@pytest.mark.asyncio
async def test_connect(client):
    r = await client.put("/api/v1/covercalibrator/0/connect")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/covercalibrator/0/connected")
    assert r2.json()["Value"] is True


@pytest.mark.asyncio
async def test_disconnect(client):
    await client.put("/api/v1/covercalibrator/0/connect")

    r = await client.put("/api/v1/covercalibrator/0/disconnect")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/covercalibrator/0/connected")
    assert r2.json()["Value"] is False


@pytest.mark.asyncio
async def test_connecting_flag(client):
    r = await client.get("/api/v1/covercalibrator/0/connecting")
    assert r.status_code == 200
    assert r.json()["Value"] is False


@pytest.mark.asyncio
async def test_cover_state(client):
    r = await client.get("/api/v1/covercalibrator/0/coverstate")
    assert r.status_code == 200
    assert r.json()["Value"] == 0


@pytest.mark.asyncio
async def test_open_cover(client):
    r = await client.put("/api/v1/covercalibrator/0/opencover")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/covercalibrator/0/coverstate")
    assert r2.json()["Value"] == 1


@pytest.mark.asyncio
async def test_close_cover(client):
    r = await client.put("/api/v1/covercalibrator/0/closecover")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/covercalibrator/0/coverstate")
    assert r2.json()["Value"] == 2


@pytest.mark.asyncio
async def test_halt_cover(client):
    r = await client.put("/api/v1/covercalibrator/0/haltcover")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/covercalibrator/0/coverstate")
    assert r2.json()["Value"] == 3


@pytest.mark.asyncio
async def test_calibrator_state(client):
    r = await client.get("/api/v1/covercalibrator/0/calibratorstate")
    assert r.status_code == 200
    assert r.json()["Value"] == 0


@pytest.mark.asyncio
async def test_brightness(client):
    r = await client.get("/api/v1/covercalibrator/0/brightness")
    assert r.status_code == 200
    assert r.json()["Value"] == 0


@pytest.mark.asyncio
async def test_max_brightness(client):
    r = await client.get("/api/v1/covercalibrator/0/maxbrightness")
    assert r.status_code == 200
    assert r.json()["Value"] == 100


@pytest.mark.asyncio
async def test_calibrator_on(client):
    r = await client.put("/api/v1/covercalibrator/0/calibratoron?Brightness=42")
    assert r.status_code == 200
    assert r.json()["Value"] == 42

    r2 = await client.get("/api/v1/covercalibrator/0/brightness")
    assert r2.json()["Value"] == 42

    r3 = await client.get("/api/v1/covercalibrator/0/calibratorstate")
    assert r3.json()["Value"] == 1


@pytest.mark.asyncio
async def test_calibrator_off(client):
    await client.put("/api/v1/covercalibrator/0/calibratoron?Brightness=42")

    r = await client.put("/api/v1/covercalibrator/0/calibratoroff")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/covercalibrator/0/brightness")
    assert r2.json()["Value"] == 0

    r3 = await client.get("/api/v1/covercalibrator/0/calibratorstate")
    assert r3.json()["Value"] == 0


@pytest.mark.asyncio
async def test_invalid_route(client):
    r = await client.get("/api/v1/covercalibrator/0/doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_wrong_http_method(client):
    r = await client.post("/api/v1/covercalibrator/0/coverstate")
    assert r.status_code == 405


@pytest.mark.asyncio
async def test_missing_driver_instance(client):
    key = ("covercalibrator", 0)
    saved = ascom_config._drivers.pop(key)

    r = await client.get("/api/v1/covercalibrator/0/coverstate")
    assert r.status_code == 500

    ascom_config._drivers[key] = saved


@pytest.mark.asyncio
async def test_invalid_int_query_param(client):
    r = await client.put("/api/v1/covercalibrator/0/calibratoron?Brightness=notanint")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_missing_required_query_param(client):
    r = await client.put("/api/v1/covercalibrator/0/calibratoron")
    assert r.status_code == 422
