from ASCOMDriver.DeviceInterfaces.IObservingConditionsV2 import IObservingConditionsV2
from ASCOMDriver.MyDeviceDriver import MyDeviceDriver


class MyObservingConditionsDriver(MyDeviceDriver, IObservingConditionsV2):

    def __init__(self):
        super().__init__(
            "MyASCOMObservingConditionsDriverV2", "My ObservingConditions Driver V2"
        )

        self.__connecting = False
        self._supported_actions = []

        # Basic environmental placeholders
        self.__average_period = 0.0
        self.__cloud_cover = 0.0
        self.__dew_point = 10.0
        self.__humidity = 50.0
        self.__pressure = 1013.25
        self.__rain_rate = 0.0
        self.__sky_brightness = 0.0

        # V2 additions
        self.__sky_quality = 21.5
        self.__star_fwhm = 3.0
        self.__sky_temperature = -20.0
        self.__temperature = 12.0

    def Connect(self):
        self.__connecting = True
        self.logger.info("Starting ObservingConditions V2 connection workflow")
        self.Connected = True
        self.__connecting = False

    def Disconnect(self):
        self.__connecting = True
        self.logger.info("Starting ObservingConditions V2 disconnection workflow")
        self.Connected = False
        self.__connecting = False

    @property
    def Name(self) -> str:
        return "My ObservingConditions Driver V2"

    @property
    def Connecting(self) -> bool:
        return self.__connecting

    @property
    def InterfaceVersion(self) -> int:
        return 2

    @property
    def AveragePeriod(self) -> float:
        self.CheckConnected("AveragePeriod")
        return self.__average_period

    @AveragePeriod.setter
    def AveragePeriod(self, value: float):
        self.CheckConnected("AveragePeriod")
        if value < 0:
            raise ValueError("AveragePeriod must be >= 0")
        self.__average_period = value

    @property
    def CloudCover(self) -> float:
        self.CheckConnected("CloudCover")
        return self.__cloud_cover

    @property
    def DewPoint(self) -> float:
        self.CheckConnected("DewPoint")
        return self.__dew_point

    @property
    def Humidity(self) -> float:
        self.CheckConnected("Humidity")
        return self.__humidity

    @property
    def Pressure(self) -> float:
        self.CheckConnected("Pressure")
        return self.__pressure

    @property
    def RainRate(self) -> float:
        self.CheckConnected("RainRate")
        return self.__rain_rate

    @property
    def SkyBrightness(self) -> float:
        self.CheckConnected("SkyBrightness")
        return self.__sky_brightness

    @property
    def SkyQuality(self) -> float:
        self.CheckConnected("SkyQuality")
        return self.__sky_quality

    @property
    def StarFWHM(self) -> float:
        self.CheckConnected("StarFWHM")
        return self.__star_fwhm

    @property
    def SkyTemperature(self) -> float:
        self.CheckConnected("SkyTemperature")
        return self.__sky_temperature

    @property
    def Temperature(self) -> float:
        self.CheckConnected("Temperature")
        return self.__temperature

    def SetupDialog(self):
        pass

    def Action(self, ActionName: str, ActionParameters: str) -> str:
        self.CheckConnected("Action")
        self._last_result = ""
        return ""

    @property
    def SupportedActions(self):
        return self._supported_actions

    def CommandBlind(self, Command: str, Raw: bool = False):
        self.CheckConnected("CommandBlind")
        raise NotImplementedError

    def CommandBool(self, Command: str, Raw: bool = False) -> bool:
        self.CheckConnected("CommandBool")
        raise NotImplementedError

    def CommandString(self, Command: str, Raw: bool = False) -> str:
        self.CheckConnected("CommandString")
        raise NotImplementedError

    def Dispose(self):
        pass
