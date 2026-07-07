from abc import ABC, abstractmethod

from .IAscomDriver import IAscomDriver
from .IDeviceControl import IDeviceControl
from .Enumerations import CameraStates, GuideDirections


class ICameraV1(IAscomDriver, IDeviceControl, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ICameraV1.cs
    """

    @abstractmethod
    def AbortExposure(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def BinX(self) -> int:
        raise NotImplementedError

    @BinX.setter
    @abstractmethod
    def BinX(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def BinY(self) -> int:
        raise NotImplementedError

    @BinY.setter
    @abstractmethod
    def BinY(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def CameraState(self) -> CameraStates:
        raise NotImplementedError

    @property
    @abstractmethod
    def CameraXSize(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def CameraYSize(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanAbortExposure(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanAsymmetricBin(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanGetCoolerPower(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanPulseGuide(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetCCDTemperature(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanStopExposure(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CCDTemperature(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def CoolerOn(self) -> bool:
        raise NotImplementedError

    @CoolerOn.setter
    @abstractmethod
    def CoolerOn(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def CoolerPower(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def ElectronsPerADU(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def FullWellCapacity(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def HasShutter(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def HeatSinkTemperature(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def ImageArray(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ImageArrayVariant(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ImageReady(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def IsPulseGuiding(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def LastExposureDuration(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def LastExposureStartTime(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def MaxADU(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def MaxBinX(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def MaxBinY(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def NumX(self) -> int:
        raise NotImplementedError

    @NumX.setter
    @abstractmethod
    def NumX(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def NumY(self) -> int:
        raise NotImplementedError

    @NumY.setter
    @abstractmethod
    def NumY(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def PixelSizeX(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def PixelSizeY(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def PulseGuide(self, Direction: GuideDirections, Duration: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def SetCCDTemperature(self) -> float:
        raise NotImplementedError

    @SetCCDTemperature.setter
    @abstractmethod
    def SetCCDTemperature(self, value: float):
        raise NotImplementedError

    @abstractmethod
    def StartExposure(self, Duration: float, Light: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def StartX(self) -> int:
        raise NotImplementedError

    @StartX.setter
    @abstractmethod
    def StartX(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def StartY(self) -> int:
        raise NotImplementedError

    @StartY.setter
    @abstractmethod
    def StartY(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def StopExposure(self):
        raise NotImplementedError
