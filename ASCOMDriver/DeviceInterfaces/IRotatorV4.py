from abc import ABC, abstractmethod


class IRotatorV4(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IRotatorV4.cs
    """

    @property
    @abstractmethod
    def Connected(self):
        """True if connected to hardware; False otherwise."""
        raise NotImplementedError

    @Connected.setter
    @abstractmethod
    def Connected(self, value):
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        """Launch driver configuration dialog."""
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

    @abstractmethod
    def Action(self, actionName: str, actionParameters: str) -> str:
        """Invoke a device‑specific custom action."""
        raise NotImplementedError

    @property
    @abstractmethod
    def CanReverse(self) -> bool:
        """True if Reverse is supported."""
        raise NotImplementedError

    @abstractmethod
    def CommandBlind(self, command: str, raw: bool = False):
        """Deprecated: send a command without waiting for a response."""
        raise NotImplementedError

    @abstractmethod
    def CommandBool(self, command: str, raw: bool = False) -> bool:
        """Deprecated: send a command and return a boolean."""
        raise NotImplementedError

    @abstractmethod
    def CommandString(self, command: str, raw: bool = False) -> str:
        """Deprecated: send a command and return a string."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Description(self) -> str:
        """Device description."""
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
        """Clean up resources."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self) -> str:
        """Long descriptive driver information."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self) -> str:
        """Driver version string 'n.n'."""
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        """Must return 4 for IRotatorV4."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        """Short driver name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self):
        """List of supported action names."""
        raise NotImplementedError

    @property
    @abstractmethod
    def MechanicalPosition(self) -> float:
        """Raw mechanical position (0–360)."""
        raise NotImplementedError

    @abstractmethod
    def MoveMechanical(self, position: float):
        """Move to a mechanical position (ignoring sync offset)."""
        raise NotImplementedError

    @abstractmethod
    def Sync(self, position: float):
        """
        Sync the rotator to a position without moving it.
        Must update and persist the sync offset.
        """
        raise NotImplementedError
