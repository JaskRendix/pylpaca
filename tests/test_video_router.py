from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.config import ascom_config
from services.video_router import get_video_router


@pytest.fixture
def client():
    app = FastAPI()
    router = get_video_router(device_number=0)
    app.include_router(router, prefix="/video/0")
    return TestClient(app)


@pytest.fixture
def mock_driver(monkeypatch):
    driver = MagicMock()

    # Connection
    driver.Connected = False

    # Basic properties
    driver.Description = "MockVideo"
    driver.DriverInfo = "MockVideoDriverInfo"
    driver.DriverVersion = "1.0"
    driver.InterfaceVersion = 2
    driver.Name = "MockVideoDriver"

    # Actions
    driver.SupportedActions = []
    driver.Action.side_effect = NotImplementedError

    # Device-specific
    driver.VideoCaptureDeviceName = "MockCapture"
    driver.ExposureMax = 10.0
    driver.ExposureMin = 1.0
    driver.FrameRate = 0
    driver.SupportedIntegrationRates = [1.0, 2.0, 4.0]
    driver.IntegrationRate = 0

    # Frame
    mock_frame = MagicMock()
    mock_frame.ImageArray = [[0]]
    mock_frame.PreviewBitmap = b""
    mock_frame.FrameNumber = 0
    mock_frame.ExposureDuration = 1.0
    mock_frame.ExposureStartTime = "2024-01-01T00:00:00"
    mock_frame.ImageMetadata = []
    driver.LastVideoFrame = mock_frame

    # Sensor
    driver.SensorName = "GENERIC_SENSOR"
    driver.SensorType = 0

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
    value = check_envelope(client.get("/video/0/connected"))
    assert value is False


def test_put_connected(client, mock_driver):
    value = check_envelope(client.put("/video/0/connected", params={"value": True}))
    assert value is True
    assert mock_driver.Connected is True


def test_description(client, mock_driver):
    value = check_envelope(client.get("/video/0/description"))
    assert value == "MockVideo"


def test_driverinfo(client, mock_driver):
    value = check_envelope(client.get("/video/0/driverinfo"))
    assert value == "MockVideoDriverInfo"


def test_driverversion(client, mock_driver):
    value = check_envelope(client.get("/video/0/driverversion"))
    assert value == "1.0"


def test_interfaceversion(client, mock_driver):
    value = check_envelope(client.get("/video/0/interfaceversion"))
    assert value == 2


def test_name(client, mock_driver):
    value = check_envelope(client.get("/video/0/name"))
    assert value == "MockVideoDriver"


def test_supportedactions(client, mock_driver):
    value = check_envelope(client.get("/video/0/supportedactions"))
    assert value == []


def test_action_not_implemented(client, mock_driver):
    r = client.put("/video/0/action/test")
    assert r.status_code == 400


def test_capture_device_name(client, mock_driver):
    value = check_envelope(client.get("/video/0/videocapturedevicename"))
    assert value == "MockCapture"


def test_exposure_limits(client, mock_driver):
    assert check_envelope(client.get("/video/0/exposuremax")) == 10.0
    assert check_envelope(client.get("/video/0/exposuremin")) == 1.0


def test_framerate(client, mock_driver):
    assert check_envelope(client.get("/video/0/framerate")) == 0


def test_supported_integration_rates(client, mock_driver):
    assert check_envelope(client.get("/video/0/supportedintegrationrates")) == [
        1.0,
        2.0,
        4.0,
    ]


def test_get_integrationrate(client, mock_driver):
    assert check_envelope(client.get("/video/0/integrationrate")) == 0


def test_put_integrationrate_valid(client, mock_driver):
    value = check_envelope(client.put("/video/0/integrationrate", params={"value": 2}))
    assert value == 2
    assert mock_driver.IntegrationRate == 2


def test_put_integrationrate_invalid(client, mock_driver):
    r = client.put("/video/0/integrationrate", params={"value": 999})
    assert r.status_code == 400


def test_lastvideoframe(client, mock_driver):
    value = check_envelope(client.get("/video/0/lastvideoframe"))
    assert value["ImageArray"] == [[0]]
    assert value["PreviewBitmap"] == ""
    assert value["FrameNumber"] == 0
    assert value["ExposureDuration"] == 1.0
    assert value["ExposureStartTime"] == "2024-01-01T00:00:00"
    assert value["ImageMetadata"] == []


def test_sensorname(client, mock_driver):
    assert check_envelope(client.get("/video/0/sensorname")) == "GENERIC_SENSOR"


def test_sensortype(client, mock_driver):
    assert check_envelope(client.get("/video/0/sensortype")) == 0
