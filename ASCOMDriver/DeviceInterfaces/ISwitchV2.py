from abc import ABC, abstractmethod


class ISwitchV2(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ISwitchV2.vb
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
        """Short description of the device."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self) -> str:
        """Long driver information string."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self) -> str:
        """Driver version in 'n.n' format."""
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        """Must return 2 for ISwitchV2."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        """Short driver name."""
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        """Optional configuration dialog."""
        raise NotImplementedError

    @abstractmethod
    def Action(self, action_name: str, action_parameters: str) -> str:
        """Execute a driver‑specific action."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self) -> list[str]:
        """List of supported action names."""
        raise NotImplementedError

    @abstractmethod
    def CommandBlind(self, command: str, raw: bool = False):
        raise NotImplementedError

    @abstractmethod
    def CommandBool(self, command: str, raw: bool = False) -> bool:
        raise NotImplementedError

    @abstractmethod
    def CommandString(self, command: str, raw: bool = False) -> str:
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
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
    def GetSwitchDescription(self, id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def CanWrite(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def GetSwitch(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def SetSwitch(self, id: int, state: bool):
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
    def GetSwitchValue(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def SetSwitchValue(self, id: int, value: float):
        raise NotImplementedError
