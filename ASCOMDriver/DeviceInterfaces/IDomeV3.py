from abc import ABC, abstractmethod

from .IDomeV2 import IDomeV2
from .IStateValueCollection import IStateValueCollection


class IDomeV3(IDomeV2, ABC):
    """ASCOM Dome V3 interface."""

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
