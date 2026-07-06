from abc import ABC, abstractmethod


class IRate(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IRate.vb
    """

    @abstractmethod
    def Dispose(self):
        """Release any resources associated with this rate object."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Maximum(self) -> float:
        """Maximum rate value."""
        raise NotImplementedError

    @Maximum.setter
    @abstractmethod
    def Maximum(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def Minimum(self) -> float:
        """Minimum rate value."""
        raise NotImplementedError

    @Minimum.setter
    @abstractmethod
    def Minimum(self, value: float):
        raise NotImplementedError
