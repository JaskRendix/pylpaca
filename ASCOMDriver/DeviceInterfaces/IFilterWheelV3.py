from abc import ABC, abstractmethod

from .IFilterWheelV2 import IFilterWheelV2
from .IStateValueCollection import IStateValueCollection


class IFilterWheelV3(IFilterWheelV2, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IFilterWheelV3.cs
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
