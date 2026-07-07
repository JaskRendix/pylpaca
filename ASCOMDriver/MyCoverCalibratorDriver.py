from ASCOMDriver.DeviceInterfaces.ICoverCalibratorV2 import ICoverCalibratorV2
from ASCOMDriver.DeviceInterfaces.Enumerations import CoverStatus, CalibratorStatus
from ASCOMDriver.MyDeviceDriver import MyDeviceDriver


class MyCoverCalibratorDriver(MyDeviceDriver, ICoverCalibratorV2):

    def __init__(self):
        super().__init__("MyASCOMCoverCalibratorDriverV2", "My CoverCalibrator Driver V2")

        self.__connecting = False
        self.__cover_state = CoverStatus.Closed
        self.__calibrator_state = CalibratorStatus.Off
        self.__brightness = 0
        self.__max_brightness = 255

    def Connect(self):
        self.__connecting = True
        self.logger.info("Starting CoverCalibrator V2 connection workflow")
        self.Connected = True
        self.__connecting = False

    def Disconnect(self):
        self.__connecting = True
        self.logger.info("Starting CoverCalibrator V2 disconnection workflow")
        self.Connected = False
        self.__connecting = False

    @property
    def Connecting(self) -> bool:
        return self.__connecting

    @property
    def CoverState(self) -> CoverStatus:
        self.CheckConnected("CoverState")
        return self.__cover_state

    def OpenCover(self):
        self.CheckConnected("OpenCover")
        if self.__cover_state != CoverStatus.Open:
            self.__cover_state = CoverStatus.Open
            self.logger.info("Cover opened")
            self._last_result = "Cover opened"

    def CloseCover(self):
        self.CheckConnected("CloseCover")
        if self.__cover_state != CoverStatus.Closed:
            self.__cover_state = CoverStatus.Closed
            self.logger.info("Cover closed")
            self._last_result = "Cover closed"

    def HaltCover(self):
        self.CheckConnected("HaltCover")
        self.logger.info("Cover halted")
        self._last_result = "Cover halted"

    @property
    def CalibratorState(self) -> CalibratorStatus:
        self.CheckConnected("CalibratorState")
        return self.__calibrator_state

    @property
    def Brightness(self) -> int:
        self.CheckConnected("Brightness")
        return self.__brightness

    @property
    def MaxBrightness(self) -> int:
        return self.__max_brightness

    def CalibratorOn(self, Brightness: int):
        self.CheckConnected("CalibratorOn")
        if Brightness < 0 or Brightness > self.__max_brightness:
            raise ValueError("Invalid brightness value")

        self.__brightness = Brightness
        self.__calibrator_state = CalibratorStatus.Ready
        self.logger.info(f"Calibrator turned on at brightness {Brightness}")
        self._last_result = f"Calibrator on ({Brightness})"

    def CalibratorOff(self):
        self.CheckConnected("CalibratorOff")
        self.__brightness = 0
        self.__calibrator_state = CalibratorStatus.Off
        self.logger.info("Calibrator turned off")
        self._last_result = "Calibrator off"

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
