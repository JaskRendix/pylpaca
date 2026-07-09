from abc import ABC, abstractmethod


class IObservingConditions(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IObservingConditions.vb
    """

    @property
    @abstractmethod
    def Connected(self) -> bool:
        """Get or set the hardware connection state."""
        raise NotImplementedError

    @Connected.setter
    @abstractmethod
    def Connected(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def Description(self) -> str:
        """Return a short ASCII description of the device."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self) -> str:
        """Return detailed driver information (multi‑line allowed)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self) -> str:
        """Return driver version in 'n.n' format."""
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        """Return the interface version (must be 1)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        """Short driver name."""
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self) -> None:
        """Launch driver configuration dialog."""
        raise NotImplementedError

    @abstractmethod
    def Action(self, action_name: str, action_parameters: str) -> str:
        """Invoke a device‑specific action."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self) -> list[str]:
        """Return list of supported action names."""
        raise NotImplementedError

    @abstractmethod
    def CommandBlind(self, command: str, raw: bool = False) -> None:
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
    def Dispose(self) -> None:
        """Release resources."""
        raise NotImplementedError

    @property
    @abstractmethod
    def AveragePeriod(self) -> float:
        """Time period (hours) over which readings are averaged."""
        raise NotImplementedError

    @AveragePeriod.setter
    @abstractmethod
    def AveragePeriod(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def CloudCover(self) -> float:
        """Percentage of sky covered by cloud (0–100)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DewPoint(self) -> float:
        """Atmospheric dew point (°C)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Humidity(self) -> float:
        """Atmospheric humidity (0–100%)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Pressure(self) -> float:
        """Atmospheric pressure (hPa)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def RainRate(self) -> float:
        """Rain rate (mm/hour)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SkyBrightness(self) -> float:
        """Sky brightness (Lux)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SkyQuality(self) -> float:
        """Sky quality (mag/arcsec²)."""
        raise NotImplementedError
