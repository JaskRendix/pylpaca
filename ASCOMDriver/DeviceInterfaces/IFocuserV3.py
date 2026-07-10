from abc import ABC, abstractmethod


class IFocuserV3(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IFocuserV3.cs
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
        """Must return 3 for IFocuserV3."""
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
        """Invoke a device-specific custom action."""
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
    def Absolute(self) -> bool:
        """True if focuser supports absolute positioning."""
        raise NotImplementedError

    @abstractmethod
    def Halt(self):
        """Stop focuser motion."""
        raise NotImplementedError

    @property
    @abstractmethod
    def IsMoving(self) -> bool:
        """True if focuser is currently moving."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Link(self) -> bool:
        """Legacy connection property (V1 compatibility)."""
        raise NotImplementedError

    @Link.setter
    @abstractmethod
    def Link(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def MaxIncrement(self) -> int:
        """Maximum allowed step increment."""
        raise NotImplementedError

    @property
    @abstractmethod
    def MaxStep(self) -> int:
        """Maximum allowed absolute step position."""
        raise NotImplementedError

    @abstractmethod
    def Move(self, position: int):
        """
        Move focuser (absolute or relative depending on Absolute).

        IFocuserV3 change:
        - Must NOT throw InvalidOperationException when TempComp is True.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def Position(self) -> int:
        """Current focuser position (absolute focusers only)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def StepSize(self) -> float:
        """Step size in microns."""
        raise NotImplementedError

    @property
    @abstractmethod
    def TempComp(self) -> bool:
        """Temperature compensation mode."""
        raise NotImplementedError

    @TempComp.setter
    @abstractmethod
    def TempComp(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def TempCompAvailable(self) -> bool:
        """True if temperature compensation is supported."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Temperature(self) -> float:
        """Ambient temperature in Celsius."""
        raise NotImplementedError
