from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.config import ascom_config
from services.nwayswitch_router import get_nwayswitch_router


@pytest.fixture
def client():
    app = FastAPI()
    router = get_nwayswitch_router(device_number=0)
    app.include_router(router, prefix="/nwayswitch/0")
    return TestClient(app)


@pytest.fixture
def mock_driver(monkeypatch):
    driver = MagicMock()

    # Connection state
    driver.Connected = False
    driver.Connect.return_value = None
    driver.Disconnect.return_value = None
    driver.Connecting = False

    # Properties
    driver.DeviceType = "NWaySwitch"
    driver.Name = "My NWaySwitch"
    driver.State = ["0", "10", "5"]

    # Actions
    driver.SetLevel.return_value = None

    def get_driver_instance(device_type, device_number):
        return driver

    monkeypatch.setattr(ascom_config, "get_driver_instance", get_driver_instance)
    return driver


def check_envelope(response):
    assert response.status_code == 200
    body = response.json()
    assert body["ClientTransactionID"] == 0
    assert body["ServerTransactionID"] == 0
    assert body["ErrorNumber"] == 0
    assert body["ErrorMessage"] == ""
    return body["Value"]


def test_get_connected(client, mock_driver):
    value = check_envelope(client.get("/nwayswitch/0/connected"))
    assert value is False


def test_set_connected(client, mock_driver):
    value = check_envelope(
        client.put("/nwayswitch/0/connected", params={"Connected": True})
    )
    assert value is True
    assert mock_driver.Connected is True


def test_connect(client, mock_driver):
    value = check_envelope(client.put("/nwayswitch/0/connect"))
    mock_driver.Connect.assert_called_once()


def test_disconnect(client, mock_driver):
    value = check_envelope(client.put("/nwayswitch/0/disconnect"))
    mock_driver.Disconnect.assert_called_once()


def test_connecting(client, mock_driver):
    value = check_envelope(client.get("/nwayswitch/0/connecting"))
    assert value is False


def test_device_type(client, mock_driver):
    value = check_envelope(client.get("/nwayswitch/0/devicetype"))
    assert value == "NWaySwitch"


def test_name(client, mock_driver):
    value = check_envelope(client.get("/nwayswitch/0/name"))
    assert value == "My NWaySwitch"


def test_state(client, mock_driver):
    value = check_envelope(client.get("/nwayswitch/0/state"))
    assert value == ["0", "10", "5"]


def test_set_level(client, mock_driver):
    value = check_envelope(client.put("/nwayswitch/0/setlevel", params={"Level": 7}))
    assert value == 7
    mock_driver.SetLevel.assert_called_once_with(7)
