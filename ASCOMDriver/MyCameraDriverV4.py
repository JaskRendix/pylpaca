from __future__ import annotations

from array import array

from .DeviceInterfaces.Enumerations import CameraStates, GuideDirections, SensorType
from .DeviceInterfaces.ICameraV4 import ICameraV4
from .MyDeviceDriver import MyDeviceDriver


class MyCameraDriverV4(MyDeviceDriver, ICameraV4):

    def __init__(self) -> None:
        super().__init__("MyASCOMCameraDriverV4", "My Camera Driver V4")

        self.__connecting: bool = False
        self.__device_state: list[str] = []

        self.__bin_x: int = 1
        self.__bin_y: int = 1
        self.__num_x: int = 100
        self.__num_y: int = 100
        self.__start_x: int = 0
        self.__start_y: int = 0

        self.__camera_state: CameraStates = CameraStates.cameraIdle
        self.__image_ready: bool = False
        self.__last_exposure_duration: float = 0.0
        self.__last_exposure_start_time: str = ""

        self.__ccd_temperature: float = 20.0
        self.__cooler_on: bool = False
        self.__set_ccd_temperature: float = 20.0

        self.__gain: int = 0
        self.__offset: int = 0
        self.__readout_mode: int = 0

        self.__exposure_counter: int = 0

        # Per-device transaction counter
        self._server_tid: int = 0

        self.__flat_image_data: array[int]
        self._allocate_buffer()

    def _allocate_buffer(self) -> None:
        if self.__num_x <= 0 or self.__num_y <= 0:
            raise ValueError("Invalid image dimensions")
        self.__flat_image_data = array("i", [0] * (self.__num_x * self.__num_y))

    @property
    def InterfaceVersion(self) -> int:
        return 4

    def Connect(self) -> None:
        self.__connecting = True
        self.Connected = True
        self.__connecting = False

    def Disconnect(self) -> None:
        self.__connecting = True
        self.Connected = False
        self.__connecting = False

    @property
    def Connecting(self) -> bool:
        return self.__connecting

    @property
    def DeviceState(self) -> list[str]:
        return self.__device_state

    def StartExposure(self, Duration: float, Light: bool) -> None:
        self.CheckConnected("StartExposure")
        self.__camera_state = CameraStates.cameraExposing
        self.__last_exposure_duration = Duration
        self.__last_exposure_start_time = "2026-07-07T00:00:00"
        self.__image_ready = False
        self.__exposure_counter += 1

        fill_val: int = self.__exposure_counter % 256
        self.__flat_image_data = array("i", [fill_val] * (self.__num_x * self.__num_y))

    def StopExposure(self) -> None:
        self.CheckConnected("StopExposure")
        self.__camera_state = CameraStates.cameraIdle
        self.__image_ready = True

    def AbortExposure(self) -> None:
        self.CheckConnected("AbortExposure")
        self.__camera_state = CameraStates.cameraIdle
        self.__image_ready = False

    @property
    def CameraState(self) -> CameraStates:
        return self.__camera_state

    @property
    def ImageReady(self) -> bool:
        return self.__image_ready

    @property
    def ImageArray(self) -> list[list[int]]:
        self.CheckConnected("ImageArray")
        return [
            list(self.__flat_image_data[i * self.__num_x : (i + 1) * self.__num_x])
            for i in range(self.__num_y)
        ]

    @property
    def ImageArrayVariant(self) -> list[list[int]]:
        return self.ImageArray

    def GetImageBytes(self) -> tuple[bytes, int, int, list[int]]:
        self.CheckConnected("ImageArray")

        raw_bytes: bytes = self.__flat_image_data.tobytes()

        data_type_enum: int = 2  # Int32
        rank: int = 2
        dimensions: list[int] = [self.__num_x, self.__num_y]

        return raw_bytes, data_type_enum, rank, dimensions

    @property
    def LastExposureDuration(self) -> float:
        return self.__last_exposure_duration

    @property
    def LastExposureStartTime(self) -> str:
        return self.__last_exposure_start_time

    @property
    def BinX(self) -> int:
        return self.__bin_x

    @BinX.setter
    def BinX(self, value: int) -> None:
        self.__bin_x = value

    @property
    def BinY(self) -> int:
        return self.__bin_y

    @BinY.setter
    def BinY(self, value: int) -> None:
        self.__bin_y = value

    @property
    def NumX(self) -> int:
        return self.__num_x

    @NumX.setter
    def NumX(self, value: int) -> None:
        self.__num_x = value
        self._allocate_buffer()

    @property
    def NumY(self) -> int:
        return self.__num_y

    @NumY.setter
    def NumY(self, value: int) -> None:
        self.__num_y = value
        self._allocate_buffer()

    @property
    def StartX(self) -> int:
        return self.__start_x

    @StartX.setter
    def StartX(self, value: int) -> None:
        self.__start_x = value

    @property
    def StartY(self) -> int:
        return self.__start_y

    @StartY.setter
    def StartY(self, value: int) -> None:
        self.__start_y = value

    @property
    def CCDTemperature(self) -> float:
        return self.__ccd_temperature

    @property
    def CanAbortExposure(self) -> bool:
        return True

    @property
    def CanAsymmetricBin(self) -> bool:
        return False

    @property
    def CanFastReadout(self) -> bool:
        return False

    @property
    def CanGetCoolerPower(self) -> bool:
        return True

    @property
    def CanPulseGuide(self) -> bool:
        return False

    @property
    def CanSetCCDTemperature(self) -> bool:
        return True

    @property
    def CanStopExposure(self) -> bool:
        return True

    @property
    def CoolerOn(self) -> bool:
        return self.__cooler_on

    @CoolerOn.setter
    def CoolerOn(self, value: bool) -> None:
        self.__cooler_on = value

    @property
    def CoolerPower(self) -> float:
        return 0.0

    @property
    def ElectronsPerADU(self) -> float:
        return 1.0

    @property
    def ExposureMax(self) -> float:
        return 60.0

    @property
    def ExposureMin(self) -> float:
        return 0.001

    @property
    def ExposureResolution(self) -> float:
        return 0.001

    @property
    def FastReadout(self) -> bool:
        return False

    @FastReadout.setter
    def FastReadout(self, value: bool) -> None:
        return None

    @property
    def FullWellCapacity(self) -> float:
        return 100000.0

    @property
    def GainMax(self) -> int:
        return 100

    @property
    def GainMin(self) -> int:
        return 0

    @property
    def Gains(self) -> list[int]:
        return [0, 50, 100]

    @property
    def HasShutter(self) -> bool:
        return False

    @property
    def HeatSinkTemperature(self) -> float:
        return 20.0

    @property
    def MaxADU(self) -> int:
        return 65535

    @property
    def MaxBinX(self) -> int:
        return 4

    @property
    def MaxBinY(self) -> int:
        return 4

    @property
    def OffsetMax(self) -> int:
        return 100

    @property
    def OffsetMin(self) -> int:
        return 0

    @property
    def Offsets(self) -> list[int]:
        return [0, 25, 50, 75, 100]

    @property
    def PercentCompleted(self) -> int:
        return 0

    @property
    def PixelSizeX(self) -> float:
        return 3.75

    @property
    def PixelSizeY(self) -> float:
        return 3.75

    @property
    def CameraXSize(self) -> int:
        return self.__num_x

    @property
    def CameraYSize(self) -> int:
        return self.__num_y

    @property
    def ReadoutModes(self) -> list[int]:
        return [0]

    @property
    def SensorName(self) -> str:
        return "MyCameraSensor"

    @property
    def SensorType(self) -> SensorType:
        return SensorType.Monochrome

    @property
    def SetCCDTemperature(self) -> float:
        return self.__set_ccd_temperature

    @SetCCDTemperature.setter
    def SetCCDTemperature(self, value: float) -> None:
        self.__set_ccd_temperature = value

    @property
    def Gain(self) -> int:
        return self.__gain

    @Gain.setter
    def Gain(self, value: int) -> None:
        self.__gain = value

    @property
    def Offset(self) -> int:
        return self.__offset

    @Offset.setter
    def Offset(self, value: int) -> None:
        self.__offset = value

    @property
    def ReadoutMode(self) -> int:
        return self.__readout_mode

    @ReadoutMode.setter
    def ReadoutMode(self, value: int) -> None:
        self.__readout_mode = value

    @property
    def BayerOffsetX(self) -> int:
        return 0

    @property
    def BayerOffsetY(self) -> int:
        return 0

    @property
    def SubExposureDuration(self) -> float:
        return 0.0

    @SubExposureDuration.setter
    def SubExposureDuration(self, value: float) -> None:
        return None

    @property
    def IsPulseGuiding(self) -> bool:
        return False

    def PulseGuide(self, Direction: GuideDirections, Duration: int) -> None:
        raise NotImplementedError("PulseGuide is not implemented")
