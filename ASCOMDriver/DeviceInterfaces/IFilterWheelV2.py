from abc import ABC, abstractmethod

from .IAscomDriver import IAscomDriver
from .IDeviceControl import IDeviceControl


class IFilterWheelV2(IAscomDriver, IDeviceControl, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IFilterWheelV2.cs
    """

    @property
    @abstractmethod
    def Connected(self) -> bool:
        raise NotImplementedError

    @Connected.setter
    @abstractmethod
    def Connected(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def Description(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        raise NotImplementedError

    @abstractmethod
    def Action(self, ActionName: str, ActionParameters: str) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def CommandBlind(self, Command: str, Raw: bool = False):
        raise NotImplementedError

    @abstractmethod
    def CommandBool(self, Command: str, Raw: bool = False) -> bool:
        raise NotImplementedError

    @abstractmethod
    def CommandString(self, Command: str, Raw: bool = False) -> str:
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def FocusOffsets(self) -> list[int]:
        raise NotImplementedError

    @property
    @abstractmethod
    def Names(self) -> list[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def Position(self) -> int:
        raise NotImplementedError

    @Position.setter
    @abstractmethod
    def Position(self, value: int):
        raise NotImplementedError
