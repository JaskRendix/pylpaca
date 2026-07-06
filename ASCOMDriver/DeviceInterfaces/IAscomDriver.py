from abc import ABC, abstractmethod


class IAscomDriver(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IAscomDriver.vb
    """

    @property
    @abstractmethod
    def Connected(self) -> bool:
        """Set True to enable the link. Set False to disable the link."""
        raise NotImplementedError

    @Connected.setter
    @abstractmethod
    def Connected(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def Description(self) -> str:
        """Returns a description of the driver."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self) -> str:
        """Human-readable information about the driver."""
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self) -> str:
        """Driver version number."""
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        """ASCOM interface version implemented by this driver."""
        raise NotImplementedError

    @property
    @abstractmethod
    def LastResult(self) -> str:
        """Last result returned by the driver."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        """Driver name."""
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        """Display the driver setup dialog."""
        raise NotImplementedError
