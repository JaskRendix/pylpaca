from .DeviceInterfaces.Enumerations import ShutterState
from .DeviceInterfaces.IDomeV2 import IDomeV2
from .MyDeviceDriver import MyDeviceDriver


class MyDomeDriver(MyDeviceDriver, IDomeV2):

    def __init__(self):
        super().__init__("MyASCOMDomeDriver", "My driver description")
        self.__shutterstatus = ShutterState.shutterClosed
        self.__slaved = False

    def AbortSlew(self):
        self.CheckConnected("AbortSlew")
        pass

    def OpenShutter(self):
        self.CheckConnected("OpenShutter")
        if self.__shutterstatus != ShutterState.shutterOpen:
            self.__shutterstatus = ShutterState.shutterOpen
            self.logger.info("Shutter opened")
            self._last_result = "Shutter opened"

    def CloseShutter(self):
        self.CheckConnected("CloseShutter")
        if self.__shutterstatus != ShutterState.shutterClosed:
            self.__shutterstatus = ShutterState.shutterClosed
            self.logger.info("Shutter closed")
            self._last_result = "Shutter closed"

    def FindHome(self):
        self.CheckConnected("FindHome")
        pass

    def Park(self):
        self.CheckConnected("Park")
        pass

    def SetPark(self):
        self.CheckConnected("SetPark")
        pass

    def SlewToAltitude(self, altitude: float):
        self.CheckConnected("SlewToAltitude")
        pass

    def SlewToAzimuth(self, azimuth: float):
        self.CheckConnected("SlewToAzimuth")
        pass

    def SyncToAzimuth(self, azimuth: float):
        self.CheckConnected("SyncToAzimuth")
        pass

    @property
    def Altitude(self) -> float:
        self.CheckConnected("Altitude")
        return 0.0

    @property
    def AtHome(self) -> bool:
        self.CheckConnected("AtHome")
        return False

    @property
    def AtPark(self) -> bool:
        self.CheckConnected("AtPark")
        return False

    @property
    def Azimuth(self) -> float:
        self.CheckConnected("Azimuth")
        return 0.0

    @property
    def CanFindHome(self) -> bool:
        return False

    @property
    def CanPark(self) -> bool:
        return False

    @property
    def CanSetAltitude(self) -> bool:
        return False

    @property
    def CanSetAzimuth(self) -> bool:
        return False

    @property
    def CanSetPark(self) -> bool:
        return False

    @property
    def CanSetShutter(self) -> bool:
        return True

    @property
    def CanSlave(self) -> bool:
        return False

    @property
    def CanSyncAzimuth(self) -> bool:
        return False

    @property
    def ShutterStatus(self) -> ShutterState:
        self.CheckConnected("ShutterStatus")
        return self.__shutterstatus

    @property
    def Slewing(self) -> bool:
        self.CheckConnected("Slewing")
        return False

    @property
    def Slaved(self) -> bool:
        return self.__slaved

    @Slaved.setter
    def Slaved(self, value: bool):
        if not self.CanSlave:
            raise ValueError("Slaving not supported")
        self.__slaved = value

    def SetupDialog(self):
        pass

    def Action(self, actionName: str, actionParameters: str) -> str:
        self.CheckConnected("Action")
        self._last_result = ""
        return ""

    def CommandBlind(self, command: str, raw: bool = False):
        self.CheckConnected("CommandBlind")
        pass

    def CommandBool(self, command: str, raw: bool = False) -> bool:
        self.CheckConnected("CommandBool")
        return False

    def CommandString(self, command: str, raw: bool = False) -> str:
        self.CheckConnected("CommandString")
        return ""

    @property
    def SupportedActions(self):
        return self._supported_actions

    def Dispose(self) -> None:
        pass


if __name__ == "__main__":
    driver = MyDomeDriver()
    print("Initial status:", driver.ShutterStatus)
    driver.Connected = True
    driver.OpenShutter()
    print(driver.ShutterStatus)
    driver.CloseShutter()
    print(driver.ShutterStatus)
