from abc import ABC, abstractmethod
from typing import Any


class IStateValue(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IStateValue.cs
    """

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
