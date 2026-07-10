from .DeviceInterfaces.Enumerations import CameraStates, GuideDirections, SensorType
from .DeviceInterfaces.ICameraV4 import ICameraV4
from .MyDeviceDriver import MyDeviceDriver


class MyCameraDriverV4(MyDeviceDriver, ICameraV4):

    def __init__(self):
        super().__init__("MyASCOMCameraDriverV4", "My Camera Driver V4")

        # V4 connection workflow
        self.__connecting = False
        self.__device_state = []

        # Basic camera state
        self.__bin_x = 1
        self.__bin_y = 1
        self.__num_x = 100
        self.__num_y = 100
        self.__start_x = 0
        self.__start_y = 0

        # Exposure state
        self.__camera_state = CameraStates.cameraIdle
        self.__image_ready = False
        self.__last_exposure_duration = 0.0
        self.__last_exposure_start_time = ""

        # Cooler / temperature
        self.__ccd_temperature = 20.0
        self.__cooler_on = False
        self.__set_ccd_temperature = 20.0

        # Gain / offset
        self.__gain = 0
        self.__offset = 0

        # Readout mode
        self.__readout_mode = 0

        # Image buffer (simple placeholder)
        self.__image_array = [[0] * self.__num_x for _ in range(self.__num_y)]

    @property
    def InterfaceVersion(self) -> int:
        return 4

    def Connect(self):
        self.__connecting = True
        self.logger.info("Starting Camera V4 connection workflow")
        self.Connected = True
        self.__connecting = False

    def Disconnect(self):
        self.__connecting = True
        self.logger.info("Starting Camera V4 disconnection workflow")
        self.Connected = False
        self.__connecting = False

    @property
    def Connecting(self):
        return self.__connecting

    @property
    def DeviceState(self):
        return self.__device_state

    def StartExposure(self, Duration: float, Light: bool):
        self.CheckConnected("StartExposure")
        self.__camera_state = CameraStates.cameraExposing
        self.__last_exposure_duration = Duration
        self.__last_exposure_start_time = "2026-07-07T00:00:00"
        self.__image_ready = False

    def StopExposure(self):
        self.CheckConnected("StopExposure")
        self.__camera_state = CameraStates.cameraIdle
        self.__image_ready = True

    def AbortExposure(self):
        self.CheckConnected("AbortExposure")
        self.__camera_state = CameraStates.cameraIdle
        self.__image_ready = False

    @property
    def CameraState(self):
        return self.__camera_state

    @property
    def ImageReady(self):
        return self.__image_ready

    @property
    def ImageArray(self):
        return self.__image_array

    @property
    def ImageArrayVariant(self):
        return self.__image_array

    @property
    def LastExposureDuration(self):
        return self.__last_exposure_duration

    @property
    def LastExposureStartTime(self):
        return self.__last_exposure_start_time

    @property
    def BinX(self):
        return self.__bin_x

    @BinX.setter
    def BinX(self, value):
        self.__bin_x = value

    @property
    def BinY(self):
        return self.__bin_y

    @BinY.setter
    def BinY(self, value):
        self.__bin_y = value

    @property
    def NumX(self):
        return self.__num_x

    @NumX.setter
    def NumX(self, value):
        self.__num_x = value

    @property
    def NumY(self):
        return self.__num_y

    @NumY.setter
    def NumY(self, value):
        self.__num_y = value

    @property
    def StartX(self):
        return self.__start_x

    @StartX.setter
    def StartX(self, value):
        self.__start_x = value

    @property
    def StartY(self):
        return self.__start_y

    @StartY.setter
    def StartY(self, value):
        self.__start_y = value

    @property
    def CCDTemperature(self):
        return self.__ccd_temperature

    @property
    def CanAbortExposure(self):
        return True

    @property
    def CanAsymmetricBin(self):
        return False

    @property
    def CanFastReadout(self):
        return False

    @property
    def CanGetCoolerPower(self):
        return True

    @property
    def CanPulseGuide(self):
        return False

    @property
    def CanSetCCDTemperature(self):
        return True

    @property
    def CanStopExposure(self):
        return True

    @property
    def CoolerOn(self):
        return self.__cooler_on

    @CoolerOn.setter
    def CoolerOn(self, value):
        self.__cooler_on = value

    @property
    def CoolerPower(self):
        return 0.0

    @property
    def ElectronsPerADU(self):
        return 1.0

    @property
    def ExposureMax(self):
        return 60.0

    @property
    def ExposureMin(self):
        return 0.001

    @property
    def ExposureResolution(self):
        return 0.001

    @property
    def FastReadout(self):
        return False

    @FastReadout.setter
    def FastReadout(self, value):
        return None

    @property
    def FullWellCapacity(self):
        return 100000.0

    @property
    def GainMax(self):
        return 100

    @property
    def GainMin(self):
        return 0

    @property
    def Gains(self):
        return [0, 50, 100]

    @property
    def HasShutter(self):
        return False

    @property
    def HeatSinkTemperature(self):
        return 20.0

    @property
    def MaxADU(self):
        return 65535

    @property
    def MaxBinX(self):
        return 4

    @property
    def MaxBinY(self):
        return 4

    @property
    def OffsetMax(self):
        return 100

    @property
    def OffsetMin(self):
        return 0

    @property
    def Offsets(self):
        return [0, 25, 50, 75, 100]

    @property
    def PercentCompleted(self):
        return 0

    @property
    def PixelSizeX(self):
        return 3.75

    @property
    def PixelSizeY(self):
        return 3.75

    @property
    def CameraXSize(self):
        return self.__num_x

    @property
    def CameraYSize(self):
        return self.__num_y

    @property
    def ReadoutModes(self):
        return [0]

    @property
    def SensorName(self):
        return "MyCameraSensor"

    @property
    def SensorType(self):
        return SensorType.Monochrome

    @property
    def SetCCDTemperature(self):
        return self.__set_ccd_temperature

    @SetCCDTemperature.setter
    def SetCCDTemperature(self, value):
        self.__set_ccd_temperature = value

    @property
    def Gain(self):
        return self.__gain

    @Gain.setter
    def Gain(self, value):
        self.__gain = value

    @property
    def Offset(self):
        return self.__offset

    @Offset.setter
    def Offset(self, value):
        self.__offset = value

    @property
    def ReadoutMode(self):
        return self.__readout_mode

    @ReadoutMode.setter
    def ReadoutMode(self, value):
        self.__readout_mode = value

    @property
    def BayerOffsetX(self):
        return 0

    @property
    def BayerOffsetY(self):
        return 0

    @property
    def SubExposureDuration(self):
        return 0.0

    @SubExposureDuration.setter
    def SubExposureDuration(self, value):
        return None

    @property
    def IsPulseGuiding(self):
        return False

    def PulseGuide(self, Direction: GuideDirections, Duration: int):
        raise NotImplementedError("PulseGuide is not implemented")
