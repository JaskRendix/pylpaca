from abc import ABC, abstractmethod

from .Enumerations import SensorType
from .ICameraV1 import ICameraV1


class ICameraV2(ICameraV1, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ICameraV2.cs
    """

    @property
    @abstractmethod
    def BayerOffsetX(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def BayerOffsetY(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanFastReadout(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def Gain(self) -> int:
        raise NotImplementedError

    @Gain.setter
    @abstractmethod
    def Gain(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def GainMax(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def GainMin(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def Gains(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def PercentCompleted(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def ReadoutMode(self) -> int:
        raise NotImplementedError

    @ReadoutMode.setter
    @abstractmethod
    def ReadoutMode(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def ReadoutModes(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def SensorName(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def SensorType(self) -> SensorType:
        raise NotImplementedError
