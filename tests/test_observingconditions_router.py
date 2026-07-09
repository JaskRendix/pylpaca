from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.config import ascom_config
from services.observingconditions_router import get_observingconditions_router


@pytest.fixture
def client():
    app = FastAPI()
    router = get_observingconditions_router(device_number=0)
    app.include_router(router, prefix="/observingconditions")
    return TestClient(app)


@pytest.fixture
def mock_driver(monkeypatch):
    driver = MagicMock()

    # Basic connection state
    driver.Connected = False
    driver.Connect.return_value = None
    driver.Disconnect.return_value = None
    driver.Connecting = False

    # V1 properties
    driver.AveragePeriod = 0.0
    driver.CloudCover = 10.0
    driver.DewPoint = 5.0
    driver.Humidity = 50.0
    driver.Pressure = 1013.25
    driver.RainRate = 0.0
    driver.SkyBrightness = 0.1

    # V2 properties
    driver.SkyQuality = 21.5
    driver.StarFWHM = 3.0
    driver.SkyTemperature = -20.0
    driver.Temperature = 12.0

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
    value = check_envelope(client.get("/observingconditions/connected"))
    assert value is False


def test_set_connected(client, mock_driver):
    value = check_envelope(
        client.put("/observingconditions/connected", params={"Connected": True})
    )
    assert value is True


def test_connect(client, mock_driver):
    value = check_envelope(client.put("/observingconditions/connect"))
    mock_driver.Connect.assert_called_once()


def test_disconnect(client, mock_driver):
    value = check_envelope(client.put("/observingconditions/disconnect"))
    mock_driver.Disconnect.assert_called_once()


def test_connecting(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/connecting"))
    assert value is False


def test_average_period_get(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/averageperiod"))
    assert value == 0.0


def test_average_period_set(client, mock_driver):
    value = check_envelope(
        client.put("/observingconditions/averageperiod", params={"AveragePeriod": 1.5})
    )
    assert value == 1.5
    assert mock_driver.AveragePeriod == 1.5


def test_cloud_cover(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/cloudcover"))
    assert value == 10.0


def test_dew_point(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/dewpoint"))
    assert value == 5.0


def test_humidity(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/humidity"))
    assert value == 50.0


def test_pressure(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/pressure"))
    assert value == 1013.25


def test_rain_rate(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/rainrate"))
    assert value == 0.0


def test_sky_brightness(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/skybrightness"))
    assert value == 0.1


def test_sky_quality(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/skyquality"))
    assert value == 21.5


def test_star_fwhm(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/starfwhm"))
    assert value == 3.0


def test_sky_temperature(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/skytemperature"))
    assert value == -20.0


def test_temperature(client, mock_driver):
    value = check_envelope(client.get("/observingconditions/temperature"))
    assert value == 12.0
