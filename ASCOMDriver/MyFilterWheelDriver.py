from ASCOMDriver.DeviceInterfaces.IFilterWheelV3 import IFilterWheelV3
from ASCOMDriver.DeviceInterfaces.IStateValueCollection import IStateValueCollection
from ASCOMDriver.MyDeviceDriver import MyDeviceDriver


class MyFilterWheelDriver(MyDeviceDriver, IFilterWheelV3):

    def __init__(self):
        super().__init__("MyASCOMFilterWheelDriverV3", "My FilterWheel Driver V3")
        self.__connecting = False
        self.__device_state = []  # placeholder

        self.__names = ["Luminance", "Red", "Green", "Blue", "Ha"]
        self.__focus_offsets = [0, 10, 12, 11, 15]
        self.__position = 0

    @property
    def InterfaceVersion(self) -> int:
        return 3

    def Connect(self):
        self.__connecting = True
        self.logger.info("Starting FilterWheel V3 connection workflow")
        self.Connected = True
        self.__connecting = False

    def Disconnect(self):
        self.__connecting = True
        self.logger.info("Starting FilterWheel V3 disconnection workflow")
        self.Connected = False
        self.__connecting = False

    @property
    def Connecting(self) -> bool:
        return self.__connecting

    @property
    def DeviceState(self) -> IStateValueCollection:
        return self.__device_state

    @property
    def FocusOffsets(self) -> list[int]:
        self.CheckConnected("FocusOffsets")
        return self.__focus_offsets

    @property
    def Names(self) -> list[str]:
        self.CheckConnected("Names")
        return self.__names

    @property
    def Position(self) -> int:
        self.CheckConnected("Position")
        return self.__position

    @Position.setter
    def Position(self, value: int):
        self.CheckConnected("Position")
        if value < 0 or value >= len(self.__names):
            raise ValueError("Invalid filter wheel position")

        if value != self.__position:
            self.__position = value
            self.logger.info(f"Filter wheel moved to position {value}")

        self._last_result = f"Position set to {value}"

    def SetupDialog(self):
        pass

    def Action(self, ActionName: str, ActionParameters: str) -> str:
        self._last_result = ""
        return ""

    def CommandBlind(self, Command: str, Raw: bool = False):
        raise NotImplementedError

    def CommandBool(self, Command: str, Raw: bool = False) -> bool:
        raise NotImplementedError

    def CommandString(self, Command: str, Raw: bool = False) -> str:
        raise NotImplementedError

    @property
    def SupportedActions(self):
        return self._supported_actions

    def Dispose(self):
        pass
