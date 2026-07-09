from ASCOMDriver.DeviceInterfaces.INWaySwitch import INWaySwitch
from ASCOMDriver.MyDeviceDriver import MyDeviceDriver


class MyNWaySwitchDriver(MyDeviceDriver, INWaySwitch):

    def __init__(self):
        super().__init__("MyASCOMNWaySwitchDriver", "My NWaySwitch Driver")

        self.__connecting = False

        self.__device_type = "NWaySwitch"
        self.__name = "My NWaySwitch"

        self.__min_value = 0
        self.__max_value = 10
        self.__current_value = 5

    def Connect(self):
        self.__connecting = True
        self.logger.info("Starting NWaySwitch connection workflow")
        self.Connected = True
        self.__connecting = False

    def Disconnect(self):
        self.__connecting = True
        self.logger.info("Starting NWaySwitch disconnection workflow")
        self.Connected = False
        self.__connecting = False

    @property
    def Connecting(self) -> bool:
        return self.__connecting

    @property
    def DeviceType(self) -> str:
        return self.__device_type

    @property
    def Name(self) -> str:
        return self.__name

    @property
    def State(self) -> list[str]:
        self.CheckConnected("State")
        return [
            str(self.__min_value),
            str(self.__max_value),
            str(self.__current_value),
        ]

    def SetLevel(self, level: int):
        self.CheckConnected("SetLevel")

        if level < self.__min_value or level > self.__max_value:
            raise ValueError("Level out of range")

        self.__current_value = level
        self.logger.info(f"NWaySwitch level set to {level}")
        self._last_result = f"Level set to {level}"

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
