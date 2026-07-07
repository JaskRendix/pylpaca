import pytest
import httpx
from fastapi import FastAPI

from services.config import ascom_config
from services.camera_router import get_camera_router


class MockCameraDriver:
    def __init__(self):
        self.Connected = False
        self._connecting = False
        self._device_state = []

        self._binx = 1
        self._biny = 1
        self._numx = 100
        self._numy = 100
        self._startx = 0
        self._starty = 0

        self._camera_state = 0
        self._image_ready = False
        self._last_exposure_duration = 0.0
        self._last_exposure_start_time = ""

        self._ccd_temperature = 20.0
        self._cooler_on = False
        self._set_ccd_temperature = 20.0

        self._gain = 0
        self._offset = 0
        self._readout_mode = 0

        self._image_array = [[0] * self._numx for _ in range(self._numy)]

    # V4 connection workflow
    def Connect(self):
        self._connecting = True
        self.Connected = True
        self._connecting = False

    def Disconnect(self):
        self._connecting = True
        self.Connected = False
        self._connecting = False

    @property
    def Connecting(self):
        return self._connecting

    @property
    def DeviceState(self):
        return self._device_state

    # Exposure
    def StartExposure(self, Duration: float, Light: bool):
        self._camera_state = 1
        self._last_exposure_duration = Duration
        self._last_exposure_start_time = "2026-07-07T00:00:00"
        self._image_ready = False

    def StopExposure(self):
        self._camera_state = 0
        self._image_ready = True

    def AbortExposure(self):
        self._camera_state = 0
        self._image_ready = False

    @property
    def CameraState(self):
        return self._camera_state

    @property
    def ImageReady(self):
        return self._image_ready

    @property
    def ImageArray(self):
        return self._image_array

    @property
    def LastExposureDuration(self):
        return self._last_exposure_duration

    @property
    def LastExposureStartTime(self):
        return self._last_exposure_start_time

    # Binning
    @property
    def BinX(self):
        return self._binx

    @BinX.setter
    def BinX(self, value):
        self._binx = value

    @property
    def BinY(self):
        return self._biny

    @BinY.setter
    def BinY(self, value):
        self._biny = value

    # ROI
    @property
    def NumX(self):
        return self._numx

    @NumX.setter
    def NumX(self, value):
        self._numx = value

    @property
    def NumY(self):
        return self._numy

    @NumY.setter
    def NumY(self, value):
        self._numy = value

    @property
    def StartX(self):
        return self._startx

    @StartX.setter
    def StartX(self, value):
        self._startx = value

    @property
    def StartY(self):
        return self._starty

    @StartY.setter
    def StartY(self, value):
        self._starty = value

    # Cooler
    @property
    def CCDTemperature(self):
        return self._ccd_temperature

    @property
    def CoolerOn(self):
        return self._cooler_on

    @CoolerOn.setter
    def CoolerOn(self, value):
        self._cooler_on = value

    @property
    def SetCCDTemperature(self):
        return self._set_ccd_temperature

    @SetCCDTemperature.setter
    def SetCCDTemperature(self, value):
        self._set_ccd_temperature = value

    # Gain / offset
    @property
    def Gain(self):
        return self._gain

    @Gain.setter
    def Gain(self, value):
        self._gain = value

    @property
    def Offset(self):
        return self._offset

    @Offset.setter
    def Offset(self, value):
        self._offset = value

    # Readout mode
    @property
    def ReadoutMode(self):
        return self._readout_mode

    @ReadoutMode.setter
    def ReadoutMode(self, value):
        self._readout_mode = value

@pytest.fixture
def app():
    ascom_config.set_driver_instance("camera", 0, MockCameraDriver())
    app = FastAPI()
    app.include_router(get_camera_router(0), prefix="/api/v1/camera/0")
    return app


@pytest.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_connect(client):
    r = await client.put("/api/v1/camera/0/connect")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/camera/0/connected")
    assert r2.json()["Value"] is True


@pytest.mark.asyncio
async def test_disconnect(client):
    await client.put("/api/v1/camera/0/connect")

    r = await client.put("/api/v1/camera/0/disconnect")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/camera/0/connected")
    assert r2.json()["Value"] is False


@pytest.mark.asyncio
async def test_connecting_flag(client):
    r = await client.get("/api/v1/camera/0/connecting")
    assert r.status_code == 200
    assert r.json()["Value"] is False


@pytest.mark.asyncio
async def test_devicestate(client):
    r = await client.get("/api/v1/camera/0/devicestate")
    assert r.status_code == 200
    assert r.json()["Value"] == []


@pytest.mark.asyncio
async def test_start_exposure(client):
    r = await client.put("/api/v1/camera/0/startexposure?Duration=5.0&Light=true")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/camera/0/camerastate")
    assert r2.json()["Value"] == 1


@pytest.mark.asyncio
async def test_stop_exposure(client):
    await client.put("/api/v1/camera/0/startexposure?Duration=5.0&Light=true")

    r = await client.put("/api/v1/camera/0/stopexposure")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/camera/0/imageready")
    assert r2.json()["Value"] is True


@pytest.mark.asyncio
async def test_abort_exposure(client):
    await client.put("/api/v1/camera/0/startexposure?Duration=5.0&Light=true")

    r = await client.put("/api/v1/camera/0/abortexposure")
    assert r.status_code == 200

    r2 = await client.get("/api/v1/camera/0/imageready")
    assert r2.json()["Value"] is False


@pytest.mark.asyncio
async def test_image_ready(client):
    r = await client.get("/api/v1/camera/0/imageready")
    assert r.status_code == 200
    assert r.json()["Value"] is False


@pytest.mark.asyncio
async def test_image_array(client):
    r = await client.get("/api/v1/camera/0/imagearray")
    assert r.status_code == 200
    assert isinstance(r.json()["Value"], list)


@pytest.mark.asyncio
async def test_set_binx(client):
    r = await client.put("/api/v1/camera/0/binx?BinX=3")
    assert r.status_code == 200
    assert r.json()["Value"] == 3

    r2 = await client.get("/api/v1/camera/0/binx")
    assert r2.json()["Value"] == 3


@pytest.mark.asyncio
async def test_set_biny(client):
    r = await client.put("/api/v1/camera/0/biny?BinY=4")
    assert r.status_code == 200
    assert r.json()["Value"] == 4

    r2 = await client.get("/api/v1/camera/0/biny")
    assert r2.json()["Value"] == 4


@pytest.mark.asyncio
async def test_set_numx(client):
    r = await client.put("/api/v1/camera/0/numx?NumX=200")
    assert r.status_code == 200
    assert r.json()["Value"] == 200

    r2 = await client.get("/api/v1/camera/0/numx")
    assert r2.json()["Value"] == 200


@pytest.mark.asyncio
async def test_set_numy(client):
    r = await client.put("/api/v1/camera/0/numy?NumY=150")
    assert r.status_code == 200
    assert r.json()["Value"] == 150

    r2 = await client.get("/api/v1/camera/0/numy")
    assert r2.json()["Value"] == 150


@pytest.mark.asyncio
async def test_set_startx(client):
    r = await client.put("/api/v1/camera/0/startx?StartX=10")
    assert r.status_code == 200
    assert r.json()["Value"] == 10

    r2 = await client.get("/api/v1/camera/0/startx")
    assert r2.json()["Value"] == 10


@pytest.mark.asyncio
async def test_set_starty(client):
    r = await client.put("/api/v1/camera/0/starty?StartY=20")
    assert r.status_code == 200
    assert r.json()["Value"] == 20

    r2 = await client.get("/api/v1/camera/0/starty")
    assert r2.json()["Value"] == 20


@pytest.mark.asyncio
async def test_set_cooler_on(client):
    r = await client.put("/api/v1/camera/0/cooleron?CoolerOn=true")
    assert r.status_code == 200
    assert r.json()["Value"] is True

    r2 = await client.get("/api/v1/camera/0/cooleron")
    assert r2.json()["Value"] is True


@pytest.mark.asyncio
async def test_set_ccd_temperature(client):
    r = await client.put("/api/v1/camera/0/setccdtemperature?SetCCDTemperature=5.5")
    assert r.status_code == 200
    assert r.json()["Value"] == 5.5

    r2 = await client.get("/api/v1/camera/0/setccdtemperature")
    assert r2.json()["Value"] == 5.5


@pytest.mark.asyncio
async def test_set_gain(client):
    r = await client.put("/api/v1/camera/0/gain?Gain=12")
    assert r.status_code == 200
    assert r.json()["Value"] == 12

    r2 = await client.get("/api/v1/camera/0/gain")
    assert r2.json()["Value"] == 12


@pytest.mark.asyncio
async def test_set_offset(client):
    r = await client.put("/api/v1/camera/0/offset?Offset=7")
    assert r.status_code == 200
    assert r.json()["Value"] == 7

    r2 = await client.get("/api/v1/camera/0/offset")
    assert r2.json()["Value"] == 7


@pytest.mark.asyncio
async def test_set_readout_mode(client):
    r = await client.put("/api/v1/camera/0/readoutmode?ReadoutMode=2")
    assert r.status_code == 200
    assert r.json()["Value"] == 2

    r2 = await client.get("/api/v1/camera/0/readoutmode")
    assert r2.json()["Value"] == 2


@pytest.mark.asyncio
async def test_invalid_route(client):
    r = await client.get("/api/v1/camera/0/doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_wrong_http_method(client):
    r = await client.post("/api/v1/camera/0/binx")
    assert r.status_code == 405


@pytest.mark.asyncio
async def test_missing_driver_instance(client):
    key = ("camera", 0)
    saved = ascom_config._drivers.pop(key)

    r = await client.get("/api/v1/camera/0/binx")
    assert r.status_code == 500

    ascom_config._drivers[key] = saved


@pytest.mark.asyncio
async def test_invalid_int_query_param(client):
    r = await client.put("/api/v1/camera/0/binx?BinX=notanint")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_missing_required_query_param(client):
    r = await client.put("/api/v1/camera/0/startexposure")
    assert r.status_code == 422
