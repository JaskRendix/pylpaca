from abc import ABC, abstractmethod


class ISwitchV3(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ISwitchV3.cs
    """

    @property
    @abstractmethod
    def Connected(self) -> bool:
        """True if connected to hardware, False otherwise."""
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
        """Must return 3 for ISwitchV3."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def MaxSwitch(self) -> int:
        """Number of switch devices (indexed 0..MaxSwitch-1)."""
        raise NotImplementedError

    @abstractmethod
    def GetSwitchName(self, id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def SetSwitchName(self, id: int, name: str):
        raise NotImplementedError

    @abstractmethod
    def GetSwitch(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def SetSwitch(self, id: int, state: bool):
        raise NotImplementedError

    @abstractmethod
    def Action(self, action_name: str, action_parameters: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def CanWrite(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def CommandBlind(self, command: str, raw: bool = False):
        """Deprecated in V3."""
        raise NotImplementedError

    @abstractmethod
    def CommandBool(self, command: str, raw: bool = False) -> bool:
        """Deprecated in V3."""
        raise NotImplementedError

    @abstractmethod
    def CommandString(self, command: str, raw: bool = False) -> str:
        """Deprecated in V3."""
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
        raise NotImplementedError

    @abstractmethod
    def GetSwitchDescription(self, id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def GetSwitchValue(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def MaxSwitchValue(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def MinSwitchValue(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def SwitchStep(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def SetSwitchValue(self, id: int, value: float):
        raise NotImplementedError
