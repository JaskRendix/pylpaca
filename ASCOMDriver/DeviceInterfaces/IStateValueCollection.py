from abc import ABC, abstractmethod
from collections.abc import Iterator

from .IStateValue import IStateValue


class IStateValueCollection(ABC):
    """ASCOM IStateValueCollection interface."""

    @abstractmethod
    def __getitem__(self, index: int) -> IStateValue:
        """Return the state value at the given index."""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of state values."""
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator[IStateValue]:
        """Return an iterator over the state values."""
        raise NotImplementedError
