# ASCOM.Interface Telescope Enumerations
# ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/master/ASCOM.DeviceInterface/Enumerations.vb

from enum import IntEnum


class AlignmentModes(IntEnum):
    algAltAz = 0
    algPolar = 1
    algGermanPolar = 2


class DriveRates(IntEnum):
    driveSidereal = 0
    driveLunar = 1
    driveSolar = 2
    driveKing = 3


class EquatorialCoordinateType(IntEnum):
    equOther = 0
    equTopocentric = 1
    equJ2000 = 2
    equJ2050 = 3
    equB1950 = 4
    # equLocalTopocentric is obsolete but maps to 1
    equLocalTopocentric = 1


class GuideDirections(IntEnum):
    guideNorth = 0
    guideSouth = 1
    guideEast = 2
    guideWest = 3


class TelescopeAxes(IntEnum):
    axisPrimary = 0
    axisSecondary = 1
    axisTertiary = 2


class PierSide(IntEnum):
    pierEast = 0
    pierUnknown = -1
    pierWest = 1


class ShutterState(IntEnum):
    shutterOpen = 0
    shutterClosed = 1
    shutterOpening = 2
    shutterClosing = 3
    shutterError = 4


class CameraStates(IntEnum):
    cameraIdle = 0
    cameraWaiting = 1
    cameraExposing = 2
    cameraReading = 3
    cameraDownload = 4
    cameraError = 5


class SensorType(IntEnum):
    Monochrome = 0
    Color = 1
    RGGB = 2
    CMYG = 3
    CMYG2 = 4
    LRGB = 5


class CoverStatus(IntEnum):
    NotPresent = 0
    Closed = 1
    Moving = 2
    Open = 3
    Unknown = 4
    Error = 5


class CalibratorStatus(IntEnum):
    NotPresent = 0
    Off = 1
    NotReady = 2
    Ready = 3
    Unknown = 4
    Error = 5


class VideoCameraFrameRate(IntEnum):
    Variable = 0
    PAL = 1
    NTSC = 2


class VideoCameraState(IntEnum):
    videoCameraRunning = 0
    videoCameraRecording = 1
    videoCameraError = 2


class Operation(IntEnum):
    Uninitialised = 0
    None_ = 1
    All = 65535
    Connect = 2
    Disconnect = 3
    StartExposure = 4
    StopExposure = 5
    AbortExposure = 6
    PulseGuide = 7
    CalibratorOff = 8
    CalibratorOn = 9
    CloseCover = 10
    OpenCover = 11
    HaltCover = 12
    FindHome = 13
    Park = 14
    SlewToAzimuth = 15
    AbortSlew = 16
    CloseShutter = 17
    OpenShutter = 18
    SlewToAltitude = 19
    Position = 20
    Move = 21
    Halt = 22
    MoveAbsolute = 23
    MoveMechanical = 24
    SetSwitch = 25
    SetSwitchValue = 26
    Unpark = 27
    MoveAxis = 28
    SideOfPier = 29
    SlewToAltAzAsync = 30
    SlewToCoordinatesAsync = 31
    SlewToTargetAsync = 32
