from fastapi import APIRouter, HTTPException

from services.config import ascom_config
from services.device_router import make_alpaca_error, make_alpaca_response


def get_telescope_router(device_number: int):
    device_type = "telescope"
    router = APIRouter()

    def make_response(value):
        return make_alpaca_response(value)

    def make_error(message, number=1):
        return make_alpaca_error(message, number)

    def call_driver(resource: str):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=make_error(str(exc)))

        try:
            attr = getattr(driver, resource)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=make_error(str(exc)))

        try:
            value = attr() if callable(attr) else attr
        except Exception as exc:
            raise HTTPException(status_code=500, detail=make_error(str(exc)))

        return make_response(value)

    @router.get("/rightascension")
    async def rightascension():
        return call_driver("RightAscension")

    @router.get("/declination")
    async def declination():
        return call_driver("Declination")

    @router.get("/siderealtime")
    async def siderealtime():
        return call_driver("SiderealTime")

    @router.get("/utcdate")
    async def utcdate():
        return call_driver("UTCDate")

    @router.get("/slewing")
    async def slewing():
        return call_driver("Slewing")

    @router.get("/tracking")
    async def get_tracking():
        return call_driver("Tracking")

    @router.put("/tracking")
    async def set_tracking(Tracking: bool):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.Tracking = Tracking
        except Exception as exc:
            raise HTTPException(status_code=500, detail=make_error(str(exc)))

        return make_response(Tracking)

    @router.get("/trackingrate")
    async def get_tracking_rate():
        return call_driver("TrackingRate")

    @router.put("/trackingrate")
    async def set_tracking_rate(TrackingRate: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.TrackingRate = TrackingRate
        except Exception as exc:
            raise HTTPException(status_code=500, detail=make_error(str(exc)))

        return make_response(TrackingRate)

    @router.put("/slewtocoordinates")
    async def slewtocoordinates(RightAscension: float, Declination: float):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.SlewToCoordinates(RightAscension, Declination)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=make_error(str(exc)))

        return make_response(True)

    @router.put("/abortslew")
    async def abortslew():
        return call_driver("AbortSlew")

    @router.get("/connected")
    async def get_connected():
        return call_driver("Connected")

    @router.put("/connected")
    async def set_connected(Connected: bool):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.Connected = Connected
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": Connected,
        }

    @router.put("/connect")
    async def connect():
        return call_driver("Connect")

    @router.put("/disconnect")
    async def disconnect():
        return call_driver("Disconnect")

    @router.get("/connecting")
    async def connecting():
        return call_driver("Connecting")

    @router.get("/devicestate")
    async def devicestate():
        return call_driver("DeviceState")

    return router
