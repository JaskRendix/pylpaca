from ASCOMDriver.DeviceInterfaces.ISwitchV3 import ISwitchV3


class MySwitchDriver(ISwitchV3):
    """
    Simple ISwitchV3 implementation.

    - 3 boolean switches (0..2)
    - All writable
    - Also exposes analogue values 0.0 / 1.0
    """

    def __init__(self, description="TestSwitch", name="MySwitchDriver"):
        self._connected = False
        self._description = description
        self._name = name
        self._driver_info = "MySwitchDriver - Test ISwitchV3 implementation"
        self._driver_version = "1.0"
        self._interface_version = 3

        self._max_switch = 3
        self._names = [f"Switch {i}" for i in range(self._max_switch)]
        self._descriptions = [f"Test switch {i}" for i in range(self._max_switch)]
        self._can_write = [True] * self._max_switch
        self._bool_states = [False] * self._max_switch
        self._values = [0.0] * self._max_switch  # 0.0 or 1.0

    @property
    def InterfaceVersion(self) -> int:
        return 3

    @property
    def Connected(self) -> bool:
        return self._connected

    @Connected.setter
    def Connected(self, value: bool):
        self._connected = bool(value)

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
        return self._interface_version

    @property
    def Name(self) -> str:
        return self._name

    def SetupDialog(self):
        # No UI in this test driver
        pass

    @property
    def MaxSwitch(self) -> int:
        return self._max_switch

    def _check_id(self, id: int):
        if not (0 <= id < self._max_switch):
            raise ValueError(f"Invalid switch id: {id}")

    def GetSwitchName(self, id: int) -> str:
        self._check_id(id)
        return self._names[id]

    def SetSwitchName(self, id: int, name: str):
        self._check_id(id)
        self._names[id] = str(name)

    def GetSwitch(self, id: int) -> bool:
        self._check_id(id)
        return self._bool_states[id]

    def SetSwitch(self, id: int, state: bool):
        self._check_id(id)
        if not self.CanWrite(id):
            raise NotImplementedError("Switch is read-only")
        self._bool_states[id] = bool(state)
        self._values[id] = 1.0 if state else 0.0

    def Action(self, action_name: str, action_parameters: str) -> str:
        # No custom actions in this test driver
        raise NotImplementedError("No actions supported")

    def CanWrite(self, id: int) -> bool:
        self._check_id(id)
        return self._can_write[id]

    def CommandBlind(self, command: str, raw: bool = False):
        # Deprecated mechanic – not implemented
        raise NotImplementedError("CommandBlind not implemented")

    def CommandBool(self, command: str, raw: bool = False) -> bool:
        raise NotImplementedError("CommandBool not implemented")

    def CommandString(self, command: str, raw: bool = False) -> str:
        raise NotImplementedError("CommandString not implemented")

    def Dispose(self):
        # Simple cleanup: disconnect
        self._connected = False

    def GetSwitchDescription(self, id: int) -> str:
        self._check_id(id)
        return self._descriptions[id]

    def GetSwitchValue(self, id: int) -> float:
        self._check_id(id)
        return self._values[id]

    def MaxSwitchValue(self, id: int) -> float:
        self._check_id(id)
        return 1.0

    def MinSwitchValue(self, id: int) -> float:
        self._check_id(id)
        return 0.0

    def SwitchStep(self, id: int) -> float:
        self._check_id(id)
        return 1.0

    def SetSwitchValue(self, id: int, value: float):
        self._check_id(id)
        if not self.CanWrite(id):
            raise NotImplementedError("Switch is read-only")
        if value < 0.0 or value > 1.0:
            raise ValueError("Value must be between 0.0 and 1.0")
        # Snap to 0.0 / 1.0 for this simple driver
        self._values[id] = 1.0 if value >= 0.5 else 0.0
        self._bool_states[id] = self._values[id] == 1.0
