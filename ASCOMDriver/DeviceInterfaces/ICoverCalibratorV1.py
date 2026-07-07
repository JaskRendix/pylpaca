from abc import ABC, abstractmethod

from .Enumerations import CoverStatus, CalibratorStatus


class ICoverCalibratorV1(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ICoverCalibratorV1.cs
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
    def SupportedActions(self):
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
    def CoverState(self) -> CoverStatus:
        raise NotImplementedError

    @abstractmethod
    def OpenCover(self):
        raise NotImplementedError

    @abstractmethod
    def CloseCover(self):
        raise NotImplementedError

    @abstractmethod
    def HaltCover(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def CalibratorState(self) -> CalibratorStatus:
        raise NotImplementedError

    @property
    @abstractmethod
    def Brightness(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def MaxBrightness(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def CalibratorOn(self, Brightness: int):
        raise NotImplementedError

    @abstractmethod
    def CalibratorOff(self):
        raise NotImplementedError
