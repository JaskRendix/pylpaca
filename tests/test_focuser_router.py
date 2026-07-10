import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ASCOMDriver.MyFocuserDriverV4 import MyFocuserDriverV4
from services.config import ascom_config
from services.focuser_router import get_focuser_router


@pytest.fixture
def client():
    # Register driver instance
    ascom_config._drivers = {("focuser", 0): MyFocuserDriverV4()}

    app = FastAPI()
    app.include_router(get_focuser_router(0))

    return TestClient(app)


def test_connected(client):
    r = client.get("/connected")
    assert r.status_code == 200
    assert r.json()["Value"] is False

    r = client.put("/connected?value=true")
    assert r.json()["Value"] is True


def test_connect_disconnect(client):
    r = client.put("/connect")
    assert r.json()["Value"] is True

    r = client.put("/disconnect")
    assert r.json()["Value"] is False


def test_metadata(client):
    assert client.get("/description").json()["Value"] == "MyFocuserDriverV4"
    assert client.get("/driverinfo").json()["Value"] == "MyFocuserDriverV4 Focuser V4"
    assert client.get("/driverversion").json()["Value"] == "1.0"
    assert client.get("/interfaceversion").json()["Value"] == 4
    assert client.get("/name").json()["Value"] == "MyFocuserDriverV4"


def test_move_absolute(client):
    client.put("/connect")
    r = client.put("/move?value=100")
    assert r.json()["Value"] == 100

    r = client.get("/position")
    assert r.json()["Value"] == 100


def test_move_out_of_range(client):
    client.put("/connect")
    r = client.put("/move?value=20000")
    assert r.status_code == 400
    assert r.json()["detail"]["ErrorMessage"] != ""


def test_halt(client):
    client.put("/connect")
    r = client.put("/halt")
    assert r.json()["Value"] is False


def test_position_not_connected(client):
    r = client.get("/position")
    assert r.status_code == 400
    assert r.json()["detail"]["ErrorMessage"] != ""


def test_capabilities(client):
    client.put("/connect")
    assert client.get("/absolute").json()["Value"] is True
    assert client.get("/maxincrement").json()["Value"] == 500
    assert client.get("/maxstep").json()["Value"] == 10000
    assert client.get("/stepsize").json()["Value"] == 5.0


def test_tempcomp(client):
    client.put("/connect")

    r = client.get("/tempcomp")
    assert r.json()["Value"] is False

    r = client.put("/tempcomp?value=true")
    assert r.json()["Value"] is True

    r = client.get("/tempcompavailable")
    assert r.json()["Value"] is True


def test_tempcomp_not_available(client):
    # Replace driver with one that has no tempcomp
    ascom_config._drivers[("focuser", 0)] = MyFocuserDriverV4()
    ascom_config._drivers[("focuser", 0)]._temp_comp_available = False

    client.put("/connect")

    r = client.put("/tempcomp?value=true")
    assert r.status_code == 400
    assert r.json()["detail"]["ErrorMessage"] != ""


def test_temperature(client):
    client.put("/connect")
    r = client.get("/temperature")
    assert isinstance(r.json()["Value"], float)


def test_supportedactions(client):
    r = client.get("/supportedactions")
    assert r.json()["Value"] == []


def test_action_not_implemented(client):
    r = client.put("/action/test")
    assert r.status_code == 400
    assert r.json()["detail"]["ErrorMessage"] != ""
