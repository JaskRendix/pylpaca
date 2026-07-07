from .DeviceInterfaces.Enumerations import (
    AlignmentModes,
    DriveRates,
    EquatorialCoordinateType,
    GuideDirections,
    PierSide,
    TelescopeAxes,
)
from .DeviceInterfaces.ITelescopeV3 import ITelescopeV3
from .MyDeviceDriver import MyDeviceDriver


class MyTelescopeDriverV3(MyDeviceDriver, ITelescopeV3):

    def __init__(self):
        super().__init__("MyASCOMTelescopeDriverV3", "My Telescope Driver V3")
        self.__connecting = False
        self.__device_state = []  # same placeholder as dome
        self.__ra = 0.0
        self.__dec = 0.0
        self.__tracking = False
        self.__tracking_rate = DriveRates.driveSidereal

    def Connect(self):
        self.__connecting = True
        self.logger.info("Starting Telescope V3 connection workflow")
        self.Connected = True
        self.__connecting = False

    def Disconnect(self):
        self.__connecting = True
        self.logger.info("Starting Telescope V3 disconnection workflow")
        self.Connected = False
        self.__connecting = False

    @property
    def Connecting(self):
        return self.__connecting

    @property
    def DeviceState(self):
        return self.__device_state

    def AbortSlew(self):
        self.CheckConnected("AbortSlew")

    @property
    def AlignmentMode(self):
        return AlignmentModes.algAltAz

    @property
    def Altitude(self):
        return 0.0

    @property
    def ApertureArea(self):
        return 0.0

    @property
    def ApertureDiameter(self):
        return 0.0

    @property
    def AtHome(self):
        return False

    @property
    def AtPark(self):
        return False

    def AxisRates(self, axis):
        raise NotImplementedError

    @property
    def Azimuth(self):
        return 0.0

    @property
    def CanFindHome(self):
        return False

    def CanMoveAxis(self, axis):
        return False

    @property
    def CanPark(self):
        return False

    @property
    def CanPulseGuide(self):
        return False

    @property
    def CanSetDeclinationRate(self):
        return False

    @property
    def CanSetGuideRates(self):
        return False

    @property
    def CanSetPark(self):
        return False

    @property
    def CanSetPierSide(self):
        return False

    @property
    def CanSetRightAscensionRate(self):
        return False

    @property
    def CanSetTracking(self):
        return True

    @property
    def CanSlew(self):
        return False

    @property
    def CanSlewAltAz(self):
        return False

    @property
    def CanSlewAltAzAsync(self):
        return False

    @property
    def CanSlewAsync(self):
        return False

    @property
    def CanSync(self):
        return False

    @property
    def CanSyncAltAz(self):
        return False

    @property
    def CanUnpark(self):
        return False

    @property
    def Declination(self):
        return self.__dec

    @property
    def DeclinationRate(self):
        return 0.0

    @DeclinationRate.setter
    def DeclinationRate(self, value):
        pass

    def DestinationSideOfPier(self, ra, dec):
        return PierSide.pierUnknown

    @property
    def DoesRefraction(self):
        return False

    @DoesRefraction.setter
    def DoesRefraction(self, value):
        pass

    @property
    def EquatorialSystem(self):
        return EquatorialCoordinateType.equLocalTopocentric

    def FindHome(self):
        pass

    @property
    def FocalLength(self):
        return 0.0

    @property
    def GuideRateDeclination(self):
        return 0.0

    @GuideRateDeclination.setter
    def GuideRateDeclination(self, value):
        pass

    @property
    def GuideRateRightAscension(self):
        return 0.0

    @GuideRateRightAscension.setter
    def GuideRateRightAscension(self, value):
        pass

    @property
    def IsPulseGuiding(self):
        return False

    def MoveAxis(self, axis, rate):
        pass

    def Park(self):
        pass

    def PulseGuide(self, direction, duration):
        pass

    @property
    def RightAscension(self):
        return self.__ra

    @property
    def RightAscensionRate(self):
        return 0.0

    @RightAscensionRate.setter
    def RightAscensionRate(self, value):
        pass

    def SetPark(self):
        pass

    @property
    def SideOfPier(self):
        return PierSide.pierUnknown

    @SideOfPier.setter
    def SideOfPier(self, value):
        pass

    @property
    def SiderealTime(self):
        return 0.0

    @property
    def SiteElevation(self):
        return 0.0

    @SiteElevation.setter
    def SiteElevation(self, value):
        pass

    @property
    def SiteLatitude(self):
        return 0.0

    @SiteLatitude.setter
    def SiteLatitude(self, value):
        pass

    @property
    def SiteLongitude(self):
        return 0.0

    @SiteLongitude.setter
    def SiteLongitude(self, value):
        pass

    @property
    def Slewing(self):
        return False

    @property
    def SlewSettleTime(self):
        return 0

    @SlewSettleTime.setter
    def SlewSettleTime(self, value):
        pass

    def SlewToAltAz(self, azimuth, altitude):
        pass

    def SlewToAltAzAsync(self, azimuth, altitude):
        pass

    def SlewToCoordinates(self, ra, dec):
        pass

    def SlewToCoordinatesAsync(self, ra, dec):
        pass

    def SlewToTarget(self):
        pass

    def SlewToTargetAsync(self):
        pass

    def SyncToAltAz(self, azimuth, altitude):
        pass

    def SyncToCoordinates(self, ra, dec):
        pass

    def SyncToTarget(self):
        pass

    @property
    def TargetDeclination(self):
        return 0.0

    @TargetDeclination.setter
    def TargetDeclination(self, value):
        pass

    @property
    def TargetRightAscension(self):
        return 0.0

    @TargetRightAscension.setter
    def TargetRightAscension(self, value):
        pass

    @property
    def Tracking(self):
        return self.__tracking

    @Tracking.setter
    def Tracking(self, value):
        self.__tracking = value

    @property
    def TrackingRate(self):
        return self.__tracking_rate

    @TrackingRate.setter
    def TrackingRate(self, value):
        self.__tracking_rate = value

    @property
    def TrackingRates(self):
        raise NotImplementedError

    def Unpark(self):
        pass

    @property
    def UTCDate(self):
        return 0.0

    @UTCDate.setter
    def UTCDate(self, value):
        pass
