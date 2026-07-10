from ASCOMDriver.DeviceInterfaces.IFocuserV4 import IFocuserV4


class MyFocuserDriverV4(IFocuserV4):
    """
    Minimal usable Focuser V4 driver.
    Wire this into your config as:  "device_driver": "MyFocuserDriverV4"
    """

    def __init__(self, **cfg):
        self._connected = False
        self._link = False  # legacy property
        self._description = cfg.get("description", "MyFocuserDriverV4")
        self._name = cfg.get("name", "MyFocuserDriverV4")
        self._driver_info = "MyFocuserDriverV4 Focuser V4"
        self._driver_version = "1.0"

        # Focuser state
        self._absolute = True
        self._position = 0
        self._max_step = 10000
        self._max_increment = 500
        self._step_size = 5.0  # microns
        self._is_moving = False

        # Temperature compensation
        self._temp_comp_available = True
        self._temp_comp = False
        self._temperature = 20.0  # dummy ambient temperature

    @property
    def Connected(self) -> bool:
        return self._connected

    @Connected.setter
    def Connected(self, value: bool):
        self._connected = bool(value)

    def Connect(self):
        self._connected = True

    def Disconnect(self):
        self._connected = False

    # Legacy property
    @property
    def Link(self) -> bool:
        return self._link

    @Link.setter
    def Link(self, value: bool):
        self._link = bool(value)
        self._connected = self._link

    @property
    def Description(self) -> str:
        return self._description

    @property
    def DriverInfo(self) -> str:
        return self._driver_info

    @property
    def DriverVersion(self) -> str:
        return self._driver_version

    @property
    def InterfaceVersion(self) -> int:
        return 4

    @property
    def Name(self) -> str:
        return self._name

    def SetupDialog(self):
        return

    def Dispose(self):
        self._connected = False

    def Action(self, actionName: str, actionParameters: str) -> str:
        raise NotImplementedError("No actions supported")

    @property
    def SupportedActions(self):
        return []

    def CommandBlind(self, command: str, raw: bool = False):
        raise NotImplementedError("CommandBlind deprecated")

    def CommandBool(self, command: str, raw: bool = False) -> bool:
        raise NotImplementedError("CommandBool deprecated")

    def CommandString(self, command: str, raw: bool = False) -> str:
        raise NotImplementedError("CommandString deprecated")

    @property
    def Absolute(self) -> bool:
        return self._absolute

    @property
    def MaxIncrement(self) -> int:
        return self._max_increment

    @property
    def MaxStep(self) -> int:
        return self._max_step

    @property
    def StepSize(self) -> float:
        return self._step_size

    @property
    def TempComp(self) -> bool:
        return self._temp_comp

    @TempComp.setter
    def TempComp(self, value: bool):
        if not self._temp_comp_available and value:
            raise Exception("Temperature compensation not available")
        self._temp_comp = bool(value)

    @property
    def TempCompAvailable(self) -> bool:
        return self._temp_comp_available

    @property
    def Temperature(self) -> float:
        return self._temperature

    @property
    def IsMoving(self) -> bool:
        return self._is_moving

    def Halt(self):
        self._is_moving = False

    def Move(self, position: int):
        """
        IFocuserV3/V4 rule:
        - MUST NOT throw InvalidOperationException when TempComp is True.
        """
        if not self._connected:
            raise Exception("Not connected")

        self._is_moving = True

        if self._absolute:
            # Absolute positioning
            if not 0 <= position <= self._max_step:
                raise ValueError("Position out of range")
            self._position = position
        else:
            # Relative positioning
            if not -self._max_increment <= position <= self._max_increment:
                raise ValueError("Relative move out of range")
            self._position = max(0, min(self._max_step, self._position + position))

        self._is_moving = False

    @property
    def Position(self) -> int:
        if not self._connected:
            raise Exception("Not connected")
        if not self._absolute:
            raise Exception("Position not available for relative focusers")
        return self._position
