from abc import ABC, abstractmethod

from .IStateValueCollection import IStateValueCollection
from .ITelescopeV3 import ITelescopeV3


class ITelescopeV4(ITelescopeV3, ABC):
    """ASCOM Telescope V4 Interface."""

    @abstractmethod
    def Connect(self):
        """Begin asynchronous connection process."""
        raise NotImplementedError

    @abstractmethod
    def Disconnect(self):
        """Begin asynchronous disconnection process."""
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
