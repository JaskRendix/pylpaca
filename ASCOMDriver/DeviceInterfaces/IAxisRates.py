from abc import ABC, abstractmethod
from collections.abc import Iterator

from .IRate import IRate


class IAxisRates(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IAxisRates.vb
    """

    @abstractmethod
    def __getitem__(self, index: int) -> IRate:
        """Return the IRate object at the given index."""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of available rates."""
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator[IRate]:
        """Return an iterator over the available rates."""
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
        """Release any resources associated with this rate collection."""
        raise NotImplementedError
