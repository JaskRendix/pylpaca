from fastapi import APIRouter, HTTPException

from services.config import ascom_config


def make_alpaca_response(value):
    return {
        "ClientTransactionID": 0,
        "ServerTransactionID": 0,
        "ErrorNumber": 0,
        "ErrorMessage": "",
        "Value": value,
    }


def make_alpaca_error(message, number=1):
    return {
        "ClientTransactionID": 0,
        "ServerTransactionID": 0,
        "ErrorNumber": number,
        "ErrorMessage": message,
        "Value": None,
    }


def make_device_router(device_type: str, device_number: int, resources: dict[str, str]):
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
            try:
                driver = ascom_config.get_driver_instance(device_type, device_number)
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc))

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

    return router
