from datetime import datetime, timezone
from typing import Any

from ASCOMDriver.DeviceInterfaces.IVideoFrame import IVideoFrame
from ASCOMDriver.DeviceInterfaces.IVideoV2 import IVideoV2


class VideoFrame(IVideoFrame):
    def __init__(
        self,
        image_array: Any,
        preview_bitmap: bytes,
        frame_number: int,
        exposure_duration: float,
        exposure_start_time: str,
        image_metadata: list[dict],
    ):
        self._image_array = image_array
        self._preview_bitmap = preview_bitmap
        self._frame_number = frame_number
        self._exposure_duration = exposure_duration
        self._exposure_start_time = exposure_start_time
        self._image_metadata = image_metadata

    @property
    def ImageArray(self) -> Any:
        return self._image_array

    @property
    def PreviewBitmap(self) -> bytes:
        return self._preview_bitmap

    @property
    def FrameNumber(self) -> int:
        return self._frame_number

    @property
    def ExposureDuration(self) -> float:
        return self._exposure_duration

    @property
    def ExposureStartTime(self) -> str:
        return self._exposure_start_time

    @property
    def ImageMetadata(self) -> list[dict]:
        return self._image_metadata


class MyVideoDriver(IVideoV2):
    """
    Minimal, usable Video V2 driver.
    Wire this into your config as `device_driver = "MyVideoDriver"`.
    """

    def __init__(self, **cfg):
        self._connected = False
        self._frame_rate = 0  # 0 = Variable
        self._integration_rates = [0.04, 0.08, 0.16, 0.32]
        self._integration_index = 0
        self._last_frame: VideoFrame | None = None
        self._sensor_name = "GENERIC_SENSOR"
        self._sensor_type = 0  # 0 = Monochrome
        self._description = cfg.get("description", "MyVideoDriver")
        self._name = cfg.get("name", "MyVideoDriver")
        self._driver_info = "MyVideoDriver Video V2"
        self._driver_version = "1.0"
        self._video_capture_device_name = cfg.get("capture_device", "VirtualCapture")
        self._frame_counter = 0

    @property
    def Connected(self) -> bool:
        return self._connected

    @Connected.setter
    def Connected(self, value: bool):
        # For V2, prefer explicit Connect/Disconnect in higher-level API,
        # but we still honour this for compatibility.
        self._connected = bool(value)

    @property
    def Description(self) -> str:
        return self._description

    @property
    def DriverInfo(self) -> str:
        return self._driver_info

    @property
    def DriverVersion(self) -> str:
        return self._driver_version

    @property
    def InterfaceVersion(self) -> int:
        return 2

    @property
    def Name(self) -> str:
        return self._name

    def Action(self, ActionName: str, ActionParameters: str) -> str:
        # No custom actions for now
        raise NotImplementedError("No actions supported")

    @property
    def SupportedActions(self) -> list[str]:
        return []

    def Dispose(self):
        # Clean-up hook; keep minimal
        self._connected = False

    @property
    def VideoCaptureDeviceName(self) -> str:
        return self._video_capture_device_name

    def SetupDialog(self):
        # No GUI in Python; stub
        return

    @property
    def ExposureMax(self) -> float:
        return max(self._integration_rates)

    @property
    def ExposureMin(self) -> float:
        return min(self._integration_rates)

    @property
    def FrameRate(self) -> int:
        return self._frame_rate

    @property
    def SupportedIntegrationRates(self) -> list[float]:
        return self._integration_rates

    @property
    def IntegrationRate(self) -> int:
        return self._integration_index

    @IntegrationRate.setter
    def IntegrationRate(self, value: int):
        if not 0 <= value < len(self._integration_rates):
            raise ValueError("Invalid integration rate index")
        self._integration_index = value

    @property
    def LastVideoFrame(self) -> IVideoFrame:
        if self._last_frame is None:
            now = datetime.now(timezone.utc).isoformat()
            self._last_frame = VideoFrame(
                image_array=[[0]],
                preview_bitmap=b"",
                frame_number=0,
                exposure_duration=self._integration_rates[self._integration_index],
                exposure_start_time=now,
                image_metadata=[],
            )
        return self._last_frame

    @property
    def SensorName(self) -> str:
        return self._sensor_name

    @property
    def SensorType(self) -> int:
        return self._sensor_type
