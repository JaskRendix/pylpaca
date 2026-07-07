from abc import ABC, abstractmethod

from .ICoverCalibratorV1 import ICoverCalibratorV1
from .Enumerations import CoverStatus, CalibratorStatus


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
