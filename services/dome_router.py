from fastapi import APIRouter, HTTPException

from services.config import ascom_config


def get_dome_router(device_number: int):
    device_type = "dome"
    router = APIRouter()

    def call_driver(resource: str):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            attr = getattr(driver, resource)
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

    @router.get("/shutterstatus")
    async def shutter_status():
        return call_driver("ShutterStatus")

    @router.put("/openshutter")
    async def open_shutter():
        return call_driver("OpenShutter")

    @router.put("/closeshutter")
    async def close_shutter():
        return call_driver("CloseShutter")

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

    return router
