import logging
from .DeviceInterfaces.IAscomDriver import AscomDriverBase


class MyDeviceDriver(AscomDriverBase):

    FORMAT = "%(asctime)-15s %(name)s %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger("MyASCOMDriver")

    def __init__(self, name: str, description: str):
        super().__init__()
        self._name = name
        self._description = description
        self._supported_actions: list[str] = []
        self._last_result: str = ""
        self._connected = False

    @property
    def Connected(self) -> bool:
        return self._connected

    @Connected.setter
    def Connected(self, value: bool):
        if value == self._connected:
            return
        self._connected = value
        state = "Connected" if value else "Disconnected"
        self.logger.info(state)

    def CheckConnected(self, caller: str):
        if not self._connected:
            raise ValueError(f"{caller} - Not connected")

    @property
    def Description(self) -> str:
        return self._description

    @property
    def Name(self) -> str:
        return self._name

    @property
    def DriverInfo(self) -> str:
        return f"{self._name} driver"

    @property
    def DriverVersion(self) -> str:
        return "1.0"

    @property
    def InterfaceVersion(self) -> int:
        return 2

    @property
    def LastResult(self) -> str:
        return self._last_result

    @property
    def SupportedActions(self) -> list[str]:
        return self._supported_actions

    def Action(self, actionName: str, actionParameters: str) -> str:
        self._last_result = ""
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

    def SetupDialog(self) -> None:
        pass

    def Dispose(self) -> None:
        pass


if __name__ == "__main__":
    d = MyDeviceDriver("Test name", "Test description")
    print(d.Connected)
    d.Connected = True
    print(d.Connected)
