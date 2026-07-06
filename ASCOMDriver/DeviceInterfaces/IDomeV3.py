from abc import ABC, abstractmethod

from .IDomeV2 import IDomeV2
from .IStateValueCollection import IStateValueCollection


class IDomeV3(IDomeV2, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IDomeV3.cs
    """

    @abstractmethod
    def Connect(self):
        """Begin connection process."""
        raise NotImplementedError

    @abstractmethod
    def Disconnect(self):
        """Begin disconnection process."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Connecting(self) -> bool:
        """True while a connection attempt is in progress."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DeviceState(self) -> IStateValueCollection:
        """Collection of device state values."""
        raise NotImplementedError
