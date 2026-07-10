from ASCOMDriver.DeviceInterfaces.IRotatorV4 import IRotatorV4


class MyRotatorDriverV4(IRotatorV4):
    """
    Minimal usable Rotator V4 driver.
    Wire this into your config as:  "device_driver": "MyRotatorDriverV4"
    """

    def __init__(self, **cfg):
        self._connected = False
        self._description = cfg.get("description", "MyRotatorDriverV4")
        self._name = cfg.get("name", "MyRotatorDriverV4")
        self._driver_info = "MyRotatorDriverV4 Rotator V4"
        self._driver_version = "1.0"

        # Rotator state
        self._mechanical_position = 0.0  # raw mechanical angle
        self._sync_offset = 0.0  # Position = mechanical + offset
        self._reverse = False
        self._step_size = 0.1  # degrees
        self._target_position = 0.0
        self._is_moving = False

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
        # No GUI in Python
        return

    def Dispose(self):
        self._connected = False

    @property
    def IsMoving(self) -> bool:
        return self._is_moving

    def Halt(self):
        self._is_moving = False

    def _finish_move(self):
        """Simulate instant movement."""
        self._is_moving = False

    def Move(self, position: float):
        """
        Relative move: Position += delta
        """
        if not self._connected:
            raise Exception("Not connected")

        self._is_moving = True
        self._target_position = (self.Position + position) % 360
        self._mechanical_position = (self._mechanical_position + position) % 360
        self._finish_move()

    def MoveAbsolute(self, position: float):
        """
        Absolute move: Position = target
        """
        if not self._connected:
            raise Exception("Not connected")

        self._is_moving = True
        self._target_position = position % 360
        # mechanical position must adjust for sync offset
        self._mechanical_position = (position - self._sync_offset) % 360
        self._finish_move()

    @property
    def MechanicalPosition(self) -> float:
        return self._mechanical_position

    @property
    def Position(self) -> float:
        """
        Synced position = mechanical + offset
        """
        return (self._mechanical_position + self._sync_offset) % 360

    @property
    def TargetPosition(self) -> float:
        return self._target_position

    @property
    def Reverse(self) -> bool:
        return self._reverse

    @Reverse.setter
    def Reverse(self, value: bool):
        self._reverse = bool(value)

    @property
    def StepSize(self) -> float:
        return self._step_size

    def Sync(self, position: float):
        """
        Sync without moving:
        offset = desired_position - mechanical_position
        """
        if not self._connected:
            raise Exception("Not connected")

        self._sync_offset = (position - self._mechanical_position) % 360

    def MoveMechanical(self, position: float):
        """
        Move ignoring sync offset.
        """
        if not self._connected:
            raise Exception("Not connected")

        self._is_moving = True
        self._mechanical_position = position % 360
        self._target_position = self.Position
        self._finish_move()

    def Action(self, actionName: str, actionParameters: str) -> str:
        raise NotImplementedError("No custom actions supported")

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
    def CanReverse(self) -> bool:
        return True
