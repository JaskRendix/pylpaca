from typing import Any

from fastapi import APIRouter, HTTPException

from services.config import ascom_config
from services.device_router import make_alpaca_error, make_alpaca_response


def get_observingconditions_router(device_number: int) -> APIRouter:
    device_type = "observingconditions"
    router = APIRouter()

    def make_response(value):
        return make_alpaca_response(value)

    def make_error(message, number=1):
        return make_alpaca_error(message, number)

    def call_driver(resource: str) -> dict[str, Any]:
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

    @router.get("/connected")
    async def get_connected() -> dict[str, Any]:
        return call_driver("Connected")

    @router.put("/connected")
    async def set_connected(Connected: bool) -> dict[str, Any]:
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.Connected = Connected
        except Exception as exc:
            raise HTTPException(status_code=500, detail=make_error(str(exc)))

        return make_response(Connected)

    @router.put("/connect")
    async def connect() -> dict[str, Any]:
        return call_driver("Connect")

    @router.put("/disconnect")
    async def disconnect() -> dict[str, Any]:
        return call_driver("Disconnect")

    @router.get("/connecting")
    async def connecting() -> dict[str, Any]:
        return call_driver("Connecting")

    @router.get("/averageperiod")
    async def get_average_period() -> dict[str, Any]:
        return call_driver("AveragePeriod")

    @router.put("/averageperiod")
    async def set_average_period(AveragePeriod: float) -> dict[str, Any]:
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.AveragePeriod = AveragePeriod
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": AveragePeriod,
        }

    @router.get("/cloudcover")
    async def cloud_cover() -> dict[str, Any]:
        return call_driver("CloudCover")

    @router.get("/dewpoint")
    async def dew_point() -> dict[str, Any]:
        return call_driver("DewPoint")

    @router.get("/humidity")
    async def humidity() -> dict[str, Any]:
        return call_driver("Humidity")

    @router.get("/pressure")
    async def pressure() -> dict[str, Any]:
        return call_driver("Pressure")

    @router.get("/rainrate")
    async def rain_rate() -> dict[str, Any]:
        return call_driver("RainRate")

    @router.get("/skybrightness")
    async def sky_brightness() -> dict[str, Any]:
        return call_driver("SkyBrightness")

    @router.get("/skyquality")
    async def sky_quality() -> dict[str, Any]:
        return call_driver("SkyQuality")

    @router.get("/starfwhm")
    async def star_fwhm() -> dict[str, Any]:
        return call_driver("StarFWHM")

    @router.get("/skytemperature")
    async def sky_temperature() -> dict[str, Any]:
        return call_driver("SkyTemperature")

    @router.get("/temperature")
    async def temperature() -> dict[str, Any]:
        return call_driver("Temperature")

    return router
