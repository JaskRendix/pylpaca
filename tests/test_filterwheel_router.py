import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.config import ascom_config
from services.filterwheel_router import get_filterwheel_router


class MockFilterWheelDriver:
    def __init__(self):
        self._connected = False
        self._position = 0
        self._focus_offsets = [0, 10, 20]
        self._names = ["Luminance", "Red", "Green"]
        self._connecting = False
        self._devicestate = {"state": "idle"}

    @property
    def FocusOffsets(self):
        return self._focus_offsets

    @property
    def Names(self):
        return self._names

    @property
    def Position(self):
        return self._position

    @Position.setter
    def Position(self, value):
        self._position = value

    @property
    def Connected(self):
        return self._connected

    @Connected.setter
    def Connected(self, value):
        self._connected = value

    def Connect(self):
        self._connecting = True
        self._connected = True
        self._connecting = False
        return True

    def Disconnect(self):
        self._connecting = True
        self._connected = False
        self._connecting = False
        return True

    @property
    def Connecting(self):
        return self._connecting

    @property
    def DeviceState(self):
        return self._devicestate


@pytest.fixture
def client():
    # Inject mock driver
    ascom_config.set_driver_instance("filterwheel", 0, MockFilterWheelDriver())

    app = FastAPI()
    router = get_filterwheel_router(0)
    app.include_router(router, prefix="/api/v1/filterwheel/0")

    return TestClient(app)


def test_focus_offsets(client):
    r = client.get("/api/v1/filterwheel/0/focusoffsets")
    assert r.status_code == 200
    assert r.json()["Value"] == [0, 10, 20]


def test_names(client):
    r = client.get("/api/v1/filterwheel/0/names")
    assert r.status_code == 200
    assert r.json()["Value"] == ["Luminance", "Red", "Green"]


def test_get_position(client):
    r = client.get("/api/v1/filterwheel/0/position")
    assert r.status_code == 200
    assert r.json()["Value"] == 0


def test_set_position(client):
    r = client.put("/api/v1/filterwheel/0/position", params={"Position": 2})
    assert r.status_code == 200
    assert r.json()["Value"] == 2

    # Verify driver state changed
    r2 = client.get("/api/v1/filterwheel/0/position")
    assert r2.json()["Value"] == 2


def test_get_connected(client):
    r = client.get("/api/v1/filterwheel/0/connected")
    assert r.status_code == 200
    assert r.json()["Value"] is False


def test_set_connected(client):
    r = client.put("/api/v1/filterwheel/0/connected", params={"Connected": True})
    assert r.status_code == 200
    assert r.json()["Value"] is True

    r2 = client.get("/api/v1/filterwheel/0/connected")
    assert r2.json()["Value"] is True


def test_connect(client):
    r = client.put("/api/v1/filterwheel/0/connect")
    assert r.status_code == 200
    assert r.json()["Value"] is True

    r2 = client.get("/api/v1/filterwheel/0/connected")
    assert r2.json()["Value"] is True


def test_disconnect(client):
    # First connect
    client.put("/api/v1/filterwheel/0/connect")

    r = client.put("/api/v1/filterwheel/0/disconnect")
    assert r.status_code == 200
    assert r.json()["Value"] is True

    r2 = client.get("/api/v1/filterwheel/0/connected")
    assert r2.json()["Value"] is False


def test_connecting_flag(client):
    # Mock driver toggles connecting internally
    r = client.get("/api/v1/filterwheel/0/connecting")
    assert r.status_code == 200
    assert r.json()["Value"] is False


def test_device_state(client):
    r = client.get("/api/v1/filterwheel/0/devicestate")
    assert r.status_code == 200
    assert r.json()["Value"] == {"state": "idle"}
