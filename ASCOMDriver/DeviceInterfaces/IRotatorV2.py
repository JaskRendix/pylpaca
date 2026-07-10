from abc import ABC, abstractmethod


class IRotatorV2(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IRotatorV2.cs
    """

    @property
    @abstractmethod
    def Connected(self):
        """True if connected to the hardware; False otherwise."""
        raise NotImplementedError

    @Connected.setter
    @abstractmethod
    def Connected(self, value):
        raise NotImplementedError

    @property
    @abstractmethod
    def Description(self):
        """Returns a description of the device."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self):
        """Descriptive and version information about this ASCOM driver."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self):
        """Major.minor version string of the driver."""
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self):
        """Interface version number. Must return 2 for RotatorV2."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self):
        """Short display name of the driver."""
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        """Launches a configuration dialog."""
        raise NotImplementedError

    @abstractmethod
    def Action(self, actionName: str, actionParameters: str) -> str:
        """Invokes a device-specific custom action."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self):
        """Returns a list of supported action names."""
        raise NotImplementedError

    @abstractmethod
    def CommandBlind(self, command: str, raw: bool = False):
        """Send a command without waiting for a response."""
        raise NotImplementedError

    @abstractmethod
    def CommandBool(self, command: str, raw: bool = False) -> bool:
        """Send a command and return a boolean response."""
        raise NotImplementedError

    @abstractmethod
    def CommandString(self, command: str, raw: bool = False) -> str:
        """Send a command and return a string response."""
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
        """Clean up resources."""
        raise NotImplementedError

    @property
    @abstractmethod
    def CanReverse(self) -> bool:
        """True if the rotator supports the Reverse property."""
        raise NotImplementedError

    @abstractmethod
    def Halt(self):
        """Immediately stop any rotator motion."""
        raise NotImplementedError

    @property
    @abstractmethod
    def IsMoving(self) -> bool:
        """True if the rotator is currently moving."""
        raise NotImplementedError

    @abstractmethod
    def Move(self, position: float):
        """Move relative to the current position."""
        raise NotImplementedError

    @abstractmethod
    def MoveAbsolute(self, position: float):
        """Move to an absolute position."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Position(self) -> float:
        """Current instantaneous rotator position in degrees."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Reverse(self) -> bool:
        """True if rotation direction must be reversed."""
        raise NotImplementedError

    @Reverse.setter
    @abstractmethod
    def Reverse(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def StepSize(self) -> float:
        """Minimum step size in degrees."""
        raise NotImplementedError

    @property
    @abstractmethod
    def TargetPosition(self) -> float:
        """Destination position angle for Move() and MoveAbsolute()."""
        raise NotImplementedError
