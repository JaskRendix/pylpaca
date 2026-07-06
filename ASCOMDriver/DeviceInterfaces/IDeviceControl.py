from abc import ABC, abstractmethod


class IDeviceControl(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/master/ASCOM.DeviceInterface/IDeviceControl.vb
    """

    @abstractmethod
    def Action(self, actionName, actionParameters):
        """Invokes the specified device-specific action."""
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self):
        """Gets the supported actions."""
        raise NotImplementedError

    @abstractmethod
    def CommandBlind(self, command, raw=False):
        """Transmits an arbitrary string to the device and does not wait for a response."""
        raise NotImplementedError

    @abstractmethod
    def CommandBool(self, command, raw=False):
        """Transmits an arbitrary string to the device and returns a boolean."""
        raise NotImplementedError

    @abstractmethod
    def CommandString(self, command, raw=False):
        """Transmits an arbitrary string to the device and returns a string."""
        raise NotImplementedError
