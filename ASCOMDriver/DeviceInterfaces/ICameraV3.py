from abc import ABC, abstractmethod

from .ICameraV2 import ICameraV2
from .Enumerations import SensorType


class ICameraV3(ICameraV2, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ICameraV3.cs
    """

    @property
    @abstractmethod
    def ExposureMax(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def ExposureMin(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def ExposureResolution(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def FastReadout(self) -> bool:
        raise NotImplementedError

    @FastReadout.setter
    @abstractmethod
    def FastReadout(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def Offset(self) -> int:
        raise NotImplementedError

    @Offset.setter
    @abstractmethod
    def Offset(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def OffsetMax(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def OffsetMin(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def Offsets(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def SubExposureDuration(self) -> float:
        raise NotImplementedError

    @SubExposureDuration.setter
    @abstractmethod
    def SubExposureDuration(self, value: float):
        raise NotImplementedError
