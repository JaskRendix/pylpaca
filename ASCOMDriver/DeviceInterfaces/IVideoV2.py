from abc import ABC, abstractmethod

from .IVideoFrame import IVideoFrame


class IVideoV2(ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/IVideoV2.cs
    """

    @property
    @abstractmethod
    def Connected(self) -> bool:
        raise NotImplementedError

    @Connected.setter
    @abstractmethod
    def Connected(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def Description(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverInfo(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def DriverVersion(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceVersion(self) -> int:
        """
        Must return 2 for IVideoV2.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def Name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def Action(self, ActionName: str, ActionParameters: str) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedActions(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def Dispose(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def VideoCaptureDeviceName(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def SetupDialog(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ExposureMax(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def ExposureMin(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def FrameRate(self) -> int:
        """
        Enum-like integer:
            0 = Variable
            1 = PAL
            2 = NTSC
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def SupportedIntegrationRates(self) -> list[float]:
        raise NotImplementedError

    @property
    @abstractmethod
    def IntegrationRate(self) -> int:
        raise NotImplementedError

    @IntegrationRate.setter
    @abstractmethod
    def IntegrationRate(self, value: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def LastVideoFrame(self) -> IVideoFrame:
        raise NotImplementedError

    @property
    @abstractmethod
    def SensorName(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def SensorType(self) -> int:
        """
        SensorType enum:
            0 = Monochrome
            1 = Color
            2 = RGGB
            3 = CMYG
            4 = CMYG2
            5 = LRGB
        """
        raise NotImplementedError
