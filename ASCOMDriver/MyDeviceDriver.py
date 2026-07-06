import logging

from .DeviceInterfaces.IAscomDriver import IAscomDriver


class MyDeviceDriver(IAscomDriver):

    FORMAT = "%(asctime)-15s %(identifier)s %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger("MyASCOMDriver")

    def __init__(self, name, description):
        self.__connectedState = False
        self.__name = name
        self.__description = description
        self.__supportedActions = []
        self.__lastResult = ""

    @property
    def Connected(self):
        return self.__connectedState

    @Connected.setter
    def Connected(self, value):
        if value == self.__connectedState:
            return

        self.__connectedState = value
        state = "Connected" if value else "Disconnected"
        self.logger.info(f"{state}")

    @property
    def IsConnected(self):
        return self.__connectedState

    def CheckConnected(self, caller: str):
        if not self.__connectedState:
            raise ValueError(f"{caller} - Not connected")

    @property
    def Description(self):
        return self.__description

    @property
    def Name(self):
        return self.__name

    @property
    def DriverInfo(self):
        return f"{self.__name} driver"

    @property
    def DriverVersion(self):
        return "1.0"

    @property
    def InterfaceVersion(self):
        return 2

    @property
    def LastResult(self):
        return self.__lastResult

    @property
    def SupportedActions(self):
        return self.__supportedActions

    def Action(self, actionName: str, actionParameters: str):
        raise NotImplementedError("No actions implemented")

    def CommandBlind(self, command: str, raw: bool = False):
        self.CheckConnected("CommandBlind")
        raise NotImplementedError("CommandBlind not implemented")

    def CommandBool(self, command: str, raw: bool = False) -> bool:
        self.CheckConnected("CommandBool")
        raise NotImplementedError("CommandBool not implemented")

    def CommandString(self, command: str, raw: bool = False) -> str:
        self.CheckConnected("CommandString")
        raise NotImplementedError("CommandString not implemented")

    def SetupDialog(self):
        pass


if __name__ == "__main__":
    d = MyDeviceDriver("Test name", "Test description")
    print(d.Connected)
    d.Connected = True
    print(d.Connected)
