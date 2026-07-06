from abc import ABC, abstractmethod

from .Enumerations import ShutterState
from .IAscomDriver import IAscomDriver
from .IDeviceControl import IDeviceControl


class IDomeV2(IAscomDriver, IDeviceControl, ABC):
    """This interface is used to handle a dome, with or without a controllable shutter, and also a roll off roof.
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/master/ASCOM.DeviceInterface/IDomeV2.vb
    """

    @abstractmethod
    def AbortSlew(self):
        raise NotImplementedError

    @abstractmethod
    def CloseShutter(self):
        raise NotImplementedError

    @abstractmethod
    def FindHome(self):
        raise NotImplementedError

    @abstractmethod
    def OpenShutter(self):
        raise NotImplementedError

    @abstractmethod
    def Park(self):
        raise NotImplementedError

    @abstractmethod
    def SetPark(self):
        raise NotImplementedError

    @abstractmethod
    def SlewToAltitude(self, altitude: float):
        raise NotImplementedError

    @abstractmethod
    def SlewToAzimuth(self, azimuth: float):
        raise NotImplementedError

    @abstractmethod
    def SyncToAzimuth(self, azimuth: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def Altitude(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def AtHome(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def AtPark(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def Azimuth(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanFindHome(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanPark(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetAltitude(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetAzimuth(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetPark(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetShutter(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSlave(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSyncAzimuth(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def ShutterStatus(self) -> ShutterState:
        raise NotImplementedError

    @property
    @abstractmethod
    def Slewing(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def Slaved(self) -> bool:
        raise NotImplementedError

    @Slaved.setter
    @abstractmethod
    def Slaved(self, value: bool):
        raise NotImplementedError
