from fastapi import APIRouter, HTTPException

from services.config import ascom_config


def get_covercalibrator_router(device_number: int):
    device_type = "covercalibrator"
    router = APIRouter()

    def call_driver(resource: str):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        try:
            attr = getattr(driver, resource)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        try:
            value = attr() if callable(attr) else attr
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": value,
        }

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

    @router.get("/coverstate")
    async def cover_state():
        return call_driver("CoverState")

    @router.put("/opencover")
    async def open_cover():
        return call_driver("OpenCover")

    @router.put("/closecover")
    async def close_cover():
        return call_driver("CloseCover")

    @router.put("/haltcover")
    async def halt_cover():
        return call_driver("HaltCover")

    @router.get("/calibratorstate")
    async def calibrator_state():
        return call_driver("CalibratorState")

    @router.get("/brightness")
    async def brightness():
        return call_driver("Brightness")

    @router.get("/maxbrightness")
    async def max_brightness():
        return call_driver("MaxBrightness")

    @router.put("/calibratoron")
    async def calibrator_on(Brightness: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.CalibratorOn(Brightness)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": Brightness,
        }

    @router.put("/calibratoroff")
    async def calibrator_off():
        return call_driver("CalibratorOff")

    return router
