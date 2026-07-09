import pytest

from ASCOMDriver.MyVideoDriver import MyVideoDriver, VideoFrame


@pytest.fixture
def drv():
    return MyVideoDriver(
        description="TestVideo", name="TestVideoDriver", capture_device="VirtualCapture"
    )


def test_connected_set_and_get(drv):
    assert drv.Connected is False
    drv.Connected = True
    assert drv.Connected is True
    drv.Connected = False
    assert drv.Connected is False


def test_description(drv):
    assert drv.Description == "TestVideo"


def test_name(drv):
    assert drv.Name == "TestVideoDriver"


def test_driver_info(drv):
    assert "Video" in drv.DriverInfo


def test_driver_version(drv):
    assert drv.DriverVersion == "1.0"


def test_interface_version(drv):
    assert drv.InterfaceVersion == 2


def test_capture_device_name(drv):
    assert drv.VideoCaptureDeviceName == "VirtualCapture"


def test_exposure_limits(drv):
    assert drv.ExposureMin == min(drv._integration_rates)
    assert drv.ExposureMax == max(drv._integration_rates)


def test_supported_integration_rates(drv):
    assert drv.SupportedIntegrationRates == drv._integration_rates


def test_integration_rate_set_valid(drv):
    drv.IntegrationRate = 2
    assert drv.IntegrationRate == 2


def test_integration_rate_set_invalid(drv):
    with pytest.raises(ValueError):
        drv.IntegrationRate = 999


def test_frame_rate_default(drv):
    assert drv.FrameRate == 0  # Variable


def test_last_video_frame_returns_frame(drv):
    frame = drv.LastVideoFrame
    assert isinstance(frame, VideoFrame)
    assert frame.FrameNumber == 0
    assert frame.ImageArray == [[0]]
    assert frame.PreviewBitmap == b""
    assert frame.ExposureDuration == drv._integration_rates[drv._integration_index]
    assert isinstance(frame.ExposureStartTime, str)
    assert frame.ImageMetadata == []


def test_last_video_frame_cached(drv):
    f1 = drv.LastVideoFrame
    f2 = drv.LastVideoFrame
    assert f1 is f2  # cached frame


def test_sensor_name(drv):
    assert drv.SensorName == "GENERIC_SENSOR"


def test_sensor_type(drv):
    assert drv.SensorType == 0  # Monochrome


def test_supported_actions_empty(drv):
    assert drv.SupportedActions == []


def test_action_not_implemented(drv):
    with pytest.raises(NotImplementedError):
        drv.Action("TestAction", "")


def test_dispose(drv):
    drv.Connected = True
    drv.Dispose()
    assert drv.Connected is False
