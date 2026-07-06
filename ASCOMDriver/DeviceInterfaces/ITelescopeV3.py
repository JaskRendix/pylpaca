from abc import ABC, abstractmethod

from .Enumerations import (
    AlignmentModes,
    DriveRates,
    EquatorialCoordinateType,
    GuideDirections,
    PierSide,
    TelescopeAxes,
)
from .IAscomDriver import IAscomDriver
from .IAxisRates import IAxisRates
from .IDeviceControl import IDeviceControl
from .ITrackingRates import ITrackingRates


class ITelescopeV3(IAscomDriver, IDeviceControl, ABC):
    """
    Ref: https://github.com/ASCOMInitiative/ASCOMPlatform/blob/main/ASCOM.DeviceInterface/ITelescopeV3.vb
    """

    @abstractmethod
    def AbortSlew(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def AlignmentMode(self) -> AlignmentModes:
        raise NotImplementedError

    @property
    @abstractmethod
    def Altitude(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def ApertureArea(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def ApertureDiameter(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def AtHome(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def AtPark(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def AxisRates(self, axis: TelescopeAxes) -> IAxisRates:
        raise NotImplementedError

    @property
    @abstractmethod
    def Azimuth(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanFindHome(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def CanMoveAxis(self, axis: TelescopeAxes) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanPark(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanPulseGuide(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetDeclinationRate(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetGuideRates(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetPark(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetPierSide(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetRightAscensionRate(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSetTracking(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSlew(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSlewAltAz(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSlewAltAzAsync(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSlewAsync(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSync(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanSyncAltAz(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def CanUnpark(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def Declination(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def DeclinationRate(self) -> float:
        raise NotImplementedError

    @DeclinationRate.setter
    @abstractmethod
    def DeclinationRate(self, value: float):
        raise NotImplementedError

    @abstractmethod
    def DestinationSideOfPier(self, ra: float, dec: float) -> PierSide:
        raise NotImplementedError

    @property
    @abstractmethod
    def DoesRefraction(self) -> bool:
        raise NotImplementedError

    @DoesRefraction.setter
    @abstractmethod
    def DoesRefraction(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def EquatorialSystem(self) -> EquatorialCoordinateType:
        raise NotImplementedError

    @abstractmethod
    def FindHome(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def FocalLength(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def GuideRateDeclination(self) -> float:
        raise NotImplementedError

    @GuideRateDeclination.setter
    @abstractmethod
    def GuideRateDeclination(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def GuideRateRightAscension(self) -> float:
        raise NotImplementedError

    @GuideRateRightAscension.setter
    @abstractmethod
    def GuideRateRightAscension(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def IsPulseGuiding(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def MoveAxis(self, axis: TelescopeAxes, rate: float):
        raise NotImplementedError

    @abstractmethod
    def Park(self):
        raise NotImplementedError

    @abstractmethod
    def PulseGuide(self, direction: GuideDirections, duration: int):
        raise NotImplementedError

    @property
    @abstractmethod
    def RightAscension(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def RightAscensionRate(self) -> float:
        raise NotImplementedError

    @RightAscensionRate.setter
    @abstractmethod
    def RightAscensionRate(self, value: float):
        raise NotImplementedError

    @abstractmethod
    def SetPark(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def SideOfPier(self) -> PierSide:
        raise NotImplementedError

    @SideOfPier.setter
    @abstractmethod
    def SideOfPier(self, value: PierSide):
        raise NotImplementedError

    @property
    @abstractmethod
    def SiderealTime(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def SiteElevation(self) -> float:
        raise NotImplementedError

    @SiteElevation.setter
    @abstractmethod
    def SiteElevation(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def SiteLatitude(self) -> float:
        raise NotImplementedError

    @SiteLatitude.setter
    @abstractmethod
    def SiteLatitude(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def SiteLongitude(self) -> float:
        raise NotImplementedError

    @SiteLongitude.setter
    @abstractmethod
    def SiteLongitude(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def Slewing(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def SlewSettleTime(self) -> int:
        raise NotImplementedError

    @SlewSettleTime.setter
    @abstractmethod
    def SlewSettleTime(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def SlewToAltAz(self, azimuth: float, altitude: float):
        raise NotImplementedError

    @abstractmethod
    def SlewToAltAzAsync(self, azimuth: float, altitude: float):
        raise NotImplementedError

    @abstractmethod
    def SlewToCoordinates(self, ra: float, dec: float):
        raise NotImplementedError

    @abstractmethod
    def SlewToCoordinatesAsync(self, ra: float, dec: float):
        raise NotImplementedError

    @abstractmethod
    def SlewToTarget(self):
        raise NotImplementedError

    @abstractmethod
    def SlewToTargetAsync(self):
        raise NotImplementedError

    @abstractmethod
    def SyncToAltAz(self, azimuth: float, altitude: float):
        raise NotImplementedError

    @abstractmethod
    def SyncToCoordinates(self, ra: float, dec: float):
        raise NotImplementedError

    @abstractmethod
    def SyncToTarget(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def TargetDeclination(self) -> float:
        raise NotImplementedError

    @TargetDeclination.setter
    @abstractmethod
    def TargetDeclination(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def TargetRightAscension(self) -> float:
        raise NotImplementedError

    @TargetRightAscension.setter
    @abstractmethod
    def TargetRightAscension(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def Tracking(self) -> bool:
        raise NotImplementedError

    @Tracking.setter
    @abstractmethod
    def Tracking(self, value: bool):
        raise NotImplementedError

    @property
    @abstractmethod
    def TrackingRate(self) -> DriveRates:
        raise NotImplementedError

    @TrackingRate.setter
    @abstractmethod
    def TrackingRate(self, value: DriveRates):
        raise NotImplementedError

    @property
    @abstractmethod
    def TrackingRates(self) -> ITrackingRates:
        raise NotImplementedError

    @abstractmethod
    def Unpark(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def UTCDate(self):
        raise NotImplementedError

    @UTCDate.setter
    @abstractmethod
    def UTCDate(self, value):
        raise NotImplementedError
