from abc import ABC, abstractmethod


class IAscomDriver(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IAscomDriver.vb
    """

    @property
    @abstractmethod
    def Connected(self) -> bool:
        """
        Set True to enable the link. Set False to disable the link.
        You can also read the property to check whether it is connected.
        """
        raise NotImplementedError

    @Connected.setter
    @abstractmethod
    def Connected(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def Description(self) -> str:
        """
        Returns a description of the driver, such as manufacturer and model number.
        Should not exceed 68 characters (FITS header compatibility).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self) -> str:
        """
        Descriptive and version information about this ASCOM driver.
        May contain line endings and be long; intended for human-readable detail.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self) -> str:
        """
        A string containing only the major and minor version of the driver.
        Must be in the form 'n.n'.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        """
        The version of this interface. Must return 2 for Alpaca-compliant drivers.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def LastResult(self) -> str:
        """
        The result of the last executed action, or an empty string if none.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        """
        Short name of the driver, for display purposes.
        """
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self) -> None:
        """
        Launches a configuration dialog for the driver.
        For Alpaca-only drivers this may be a no-op.
        """
        raise NotImplementedError

    @abstractmethod
    def Action(self, action_name: str, action_parameters: str) -> str:
        """
        Vendor-specific command interface.

        Allows drivers to implement custom actions beyond the standard ASCOM set.
        Returns a string result.
        """
        raise NotImplementedError

    @abstractmethod
    def Dispose(self) -> None:
        """
        Release hardware resources (serial ports, sockets, etc.).
        Optional but recommended for real hardware drivers.
        """
        raise NotImplementedError


class AscomDriverBase(IAscomDriver):
    """
    Convenience base class providing sane defaults for common members.
    Concrete drivers can inherit from this instead of IAscomDriver directly.
    """

    def __init__(self):
        self._connected: bool = False
        self._last_result: str = ""
        self._name: str = self.__class__.__name__
        self._description: str = self.__class__.__doc__ or self.__class__.__name__
        self._driver_info: str = f"{self._name} ASCOM Alpaca driver"
        self._driver_version: str = "1.0"  # override in concrete driver if needed

    @property
    def Connected(self) -> bool:
        return self._connected

    @Connected.setter
    def Connected(self, value: bool):
        self._connected = bool(value)

    @property
    def Description(self) -> str:
        return self._description

    @property
    def DriverInfo(self) -> str:
        return self._driver_info

    @property
    def DriverVersion(self) -> str:
        # Must be in 'n.n' format; override if you need a different version.
        return self._driver_version

    @property
    def InterfaceVersion(self) -> int:
        # ASCOM Alpaca interface version is 2.
        return 2

    @property
    def LastResult(self) -> str:
        return self._last_result

    @property
    def Name(self) -> str:
        return self._name

    def SetupDialog(self) -> None:
        # Alpaca drivers typically don't show GUI dialogs; override if needed
        pass

    def Action(self, action_name: str, action_parameters: str) -> str:
        # Default implementation: no custom actions
        self._last_result = ""
        raise NotImplementedError(f"Action '{action_name}' not implemented")

    def Dispose(self) -> None:
        # Override to release hardware resources
        pass
