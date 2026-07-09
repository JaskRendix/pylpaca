from abc import ABC, abstractmethod


class INWaySwitch(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/INWaySwitch.vb
    """

    @property
    @abstractmethod
    def DeviceType(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def State(self) -> list[str]:
        """
        Returns a string array:
        [
            min_value,
            max_value,
            current_value
        ]
        """
        raise NotImplementedError
