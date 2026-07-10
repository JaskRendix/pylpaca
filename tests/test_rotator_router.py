import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ASCOMDriver.MyRotatorDriverV4 import MyRotatorDriverV4
from services.config import ascom_config
from services.rotator_router import get_rotator_router


@pytest.fixture
def client():
    ascom_config._drivers = {("rotator", 0): MyRotatorDriverV4()}

    app = FastAPI()
    app.include_router(get_rotator_router(0))

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
    assert client.get("/description").json()["Value"] == "MyRotatorDriverV4"
    assert client.get("/driverinfo").json()["Value"] == "MyRotatorDriverV4 Rotator V4"
    assert client.get("/driverversion").json()["Value"] == "1.0"
    assert client.get("/interfaceversion").json()["Value"] == 4
    assert client.get("/name").json()["Value"] == "MyRotatorDriverV4"


def test_move_relative(client):
    client.put("/connect")
    r = client.put("/move?value=15")
    assert r.status_code == 200
    assert isinstance(r.json()["Value"], float)


def test_moveabsolute(client):
    client.put("/connect")
    r = client.put("/moveabsolute?value=123")
    assert r.status_code == 200
    assert r.json()["Value"] == 123


def test_movemechanical(client):
    client.put("/connect")
    r = client.put("/movemechanical?value=45")
    assert r.status_code == 200
    assert r.json()["Value"] == 45


def test_sync(client):
    client.put("/connect")
    r = client.put("/sync?value=80")
    assert r.status_code == 200
    assert isinstance(r.json()["Value"], float)


def test_move_not_connected(client):
    r = client.put("/move?value=10")
    assert r.status_code == 400
    assert r.json()["detail"]["ErrorMessage"] != ""


def test_position(client):
    client.put("/connect")
    client.put("/moveabsolute?value=200")
    r = client.get("/position")
    assert r.json()["Value"] == 200


def test_mechanicalposition(client):
    client.put("/connect")
    client.put("/movemechanical?value=50")
    r = client.get("/mechanicalposition")
    assert r.json()["Value"] == 50


def test_targetposition(client):
    client.put("/connect")
    client.put("/moveabsolute?value=33")
    r = client.get("/targetposition")
    assert r.json()["Value"] == 33


def test_reverse(client):
    client.put("/connect")

    r = client.get("/reverse")
    assert r.json()["Value"] is False

    r = client.put("/reverse?value=true")
    assert r.json()["Value"] is True


def test_stepsize(client):
    client.put("/connect")
    r = client.get("/stepsize")
    assert r.json()["Value"] == 0.1


def test_halt(client):
    client.put("/connect")
    r = client.put("/halt")
    assert r.json()["Value"] is False


def test_supportedactions(client):
    r = client.get("/supportedactions")
    assert r.json()["Value"] == []


def test_action_not_implemented(client):
    r = client.put("/action/test")
    assert r.status_code == 400
    assert r.json()["detail"]["ErrorMessage"] != ""
