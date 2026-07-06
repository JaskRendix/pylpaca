from fastapi import APIRouter, HTTPException

from services.config import ascom_config


def get_dome_router(device_number: int):
    router = APIRouter()

    def call_driver(resource: str):
        # Always fetch the correct driver instance
        try:
            driver = ascom_config.get_driver_instance("dome", device_number)
        except Exception:
            raise HTTPException(status_code=500, detail="Driver not loaded")

        attr = getattr(driver, resource, None)
        if attr is None:
            raise HTTPException(status_code=404, detail=f"Unknown resource {resource}")

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
            driver = ascom_config.get_driver_instance("dome", device_number)
        except Exception:
            raise HTTPException(status_code=500, detail="Driver not loaded")

        try:
            setattr(driver, "Connected", Connected)
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
