from abc import ABC, abstractmethod


class IRotatorV3(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IRotatorV3.cs
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
        """Device description (max 64 chars)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self):
        """Long descriptive driver information."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self):
        """Driver version string 'n.n'."""
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self):
        """Must return 3 for IRotatorV3."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self):
        """Short driver name."""
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        """Launch driver configuration dialog."""
        raise NotImplementedError

    @abstractmethod
    def Action(self, actionName: str, actionParameters: str) -> str:
        """Invoke a device‑specific custom action."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self):
        """List of supported action names."""
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
        """Must always return True for IRotatorV3."""
        raise NotImplementedError

    @abstractmethod
    def Halt(self):
        """Stop any rotator motion."""
        raise NotImplementedError

    @property
    @abstractmethod
    def IsMoving(self) -> bool:
        """True if the rotator is currently moving."""
        raise NotImplementedError

    @abstractmethod
    def Move(self, position: float):
        """Move relative to current position."""
        raise NotImplementedError

    @abstractmethod
    def MoveAbsolute(self, position: float):
        """Move to an absolute position."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Position(self) -> float:
        """Synced position (mechanical + offset)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Reverse(self) -> bool:
        """True if rotation direction is reversed."""
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
        """Destination position for Move / MoveAbsolute."""
        raise NotImplementedError

    @property
    @abstractmethod
    def MechanicalPosition(self) -> float:
        """Raw mechanical position (0–360)."""
        raise NotImplementedError

    @abstractmethod
    def Sync(self, position: float):
        """
        Sync the rotator to a position without moving it.
        Must update and persist the sync offset.
        """
        raise NotImplementedError

    @abstractmethod
    def MoveMechanical(self, position: float):
        """
        Move to a mechanical position (ignoring sync offset).
        Introduced in IRotatorV3.
        """
        raise NotImplementedError
