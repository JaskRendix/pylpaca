from abc import ABC, abstractmethod

from .Enumerations import CalibratorStatus, CoverStatus
from .ICoverCalibratorV1 import ICoverCalibratorV1


class ICoverCalibratorV2(ICoverCalibratorV1, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ICoverCalibratorV2.cs
    """

    @abstractmethod
    def Connect(self):
        raise NotImplementedError

    @abstractmethod
    def Disconnect(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Connecting(self) -> bool:
        raise NotImplementedError
