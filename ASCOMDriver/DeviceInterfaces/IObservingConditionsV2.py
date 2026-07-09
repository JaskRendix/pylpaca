from abc import ABC, abstractmethod

# Import your existing V1 interface
from ASCOMDriver.DeviceInterfaces.IObservingConditions import IObservingConditions


class IObservingConditionsV2(IObservingConditions, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IObservingConditionsV2.cs
    """

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        """Return interface version (must be 2)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SkyQuality(self) -> float:
        """Sky quality (mag/arcsec²)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def StarFWHM(self) -> float:
        """Seeing measured as star FWHM (arcseconds)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SkyTemperature(self) -> float:
        """Sky temperature (°C)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Temperature(self) -> float:
        """Ambient temperature (°C)."""
        raise NotImplementedError
