from fastapi import APIRouter, HTTPException

from services.config import ascom_config


def make_device_router(device_type: str, device_number: int, resources: dict[str, str]):
    """
    resources: mapping of endpoint name → driver attribute/method name
    e.g. {"shutterstatus": "ShutterStatus"}
    """
    router = APIRouter()

    def call_driver(resource: str):
        driver = ascom_config.get_driver_instance(device_type, device_number)
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

    # Example: you can expand this per device type
    if device_type == "dome":

        @router.get("/shutterstatus")
        async def shutterstatus():
            return call_driver(resources["shutterstatus"])

        @router.put("/openshutter")
        async def openshutter():
            return call_driver(resources["openshutter"])

        @router.put("/closeshutter")
        async def closeshutter():
            return call_driver(resources["closeshutter"])

        @router.get("/connected")
        async def get_connected():
            return call_driver("Connected")

        @router.put("/connected")
        async def set_connected(Connected: bool):
            driver = ascom_config.get_driver_instance(device_type, device_number)
            try:
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

    # For telescope/camera/etc, you’d add similar blocks

    return router
