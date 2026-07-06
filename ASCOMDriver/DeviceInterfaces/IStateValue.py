from abc import ABC, abstractmethod
from typing import Any


class IStateValue(ABC):
    """ASCOM IStateValue interface."""

    @property
    @abstractmethod
    def Name(self) -> str:
        """Name of the state value."""
        raise NotImplementedError

    @property
    @abstractmethod
    def Value(self) -> Any:
        """Value associated with the state name."""
        raise NotImplementedError
