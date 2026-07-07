from abc import ABC, abstractmethod

from .ICameraV3 import ICameraV3
from .IStateValueCollection import IStateValueCollection


class ICameraV4(ICameraV3, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ICameraV4.cs
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

    @property
    @abstractmethod
    def DeviceState(self) -> IStateValueCollection:
        raise NotImplementedError
