from .DeviceInterfaces.Enumerations import ShutterState
from .DeviceInterfaces.IDomeV2 import IDomeV2
from .MyDeviceDriver import MyDeviceDriver


class MyDomeDriver(MyDeviceDriver, IDomeV2):

    def __init__(self):
        super().__init__("MyASCOMDomeDriver", "My driver description")
        self.__shutterstatus = ShutterState.shutterClosed
        self.__slaved = False

    def AbortSlew(self):
        pass

    def OpenShutter(self):
        if self.__shutterstatus != ShutterState.shutterOpen:
            self.__shutterstatus = ShutterState.shutterOpen
            self.logger.info("Shutter opened")

    def CloseShutter(self):
        if self.__shutterstatus != ShutterState.shutterClosed:
            self.__shutterstatus = ShutterState.shutterClosed
            self.logger.info("Shutter closed")

    def FindHome(self):
        pass

    def Park(self):
        pass

    def SetPark(self):
        pass

    def SlewToAltitude(self, altitude: float):
        pass

    def SlewToAzimuth(self, azimuth: float):
        pass

    def SyncToAzimuth(self, azimuth: float):
        pass

    @property
    def Altitude(self) -> float:
        return 0.0

    @property
    def AtHome(self) -> bool:
        return False

    @property
    def AtPark(self) -> bool:
        return False

    @property
    def Azimuth(self) -> float:
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
        return self.__shutterstatus

    @property
    def Slewing(self) -> bool:
        return False

    @property
    def Slaved(self) -> bool:
        return self.__slaved

    @Slaved.setter
    def Slaved(self, value: bool):
        self.__slaved = value

    @property
    def DriverInfo(self):
        return "My Dome Driver"

    @property
    def DriverVersion(self):
        return "1.0"

    @property
    def InterfaceVersion(self):
        return 2

    @property
    def LastResult(self):
        return ""

    def SetupDialog(self):
        pass

    def Action(self, actionName: str, actionParameters: str) -> str:
        # Implement custom actions here
        return ""

    def CommandBlind(self, command: str, raw: bool = False):
        # Execute a command without returning a value
        pass

    def CommandBool(self, command: str, raw: bool = False) -> bool:
        # Execute a command and return True/False
        return False

    def CommandString(self, command: str, raw: bool = False) -> str:
        # Execute a command and return a string
        return ""

    @property
    def SupportedActions(self):
        return []


if __name__ == "__main__":
    driver = MyDomeDriver()
    print("Initial status:", driver.ShutterStatus)
    driver.OpenShutter()
    print(driver.ShutterStatus)
    driver.CloseShutter()
    print(driver.ShutterStatus)
