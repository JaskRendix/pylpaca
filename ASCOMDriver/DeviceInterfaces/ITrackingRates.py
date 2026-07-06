from abc import ABC, abstractmethod
from collections.abc import Iterator

from .Enumerations import DriveRates


class ITrackingRates(ABC):
    """ASCOM ITrackingRates interface."""

    @abstractmethod
    def __getitem__(self, index: int) -> DriveRates:
        """Return the DriveRates value at the given index."""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of available tracking rates."""
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator[DriveRates]:
        """Return an iterator over the available tracking rates."""
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
        """Release any resources associated with this tracking rate collection."""
        raise NotImplementedError
