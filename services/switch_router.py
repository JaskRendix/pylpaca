from fastapi import APIRouter, HTTPException

from ASCOMDriver.DeviceInterfaces.ISwitchV3 import ISwitchV3
from services.config import ascom_config


def make_response(value):
    return {
        "ClientTransactionID": 0,
        "ServerTransactionID": 0,
        "ErrorNumber": 0,
        "ErrorMessage": "",
        "Value": value,
    }


def make_error(message, number=1):
    return {
        "ClientTransactionID": 0,
        "ServerTransactionID": 0,
        "ErrorNumber": number,
        "ErrorMessage": message,
        "Value": None,
    }


def get_switch_router(device_number: int) -> APIRouter:
    router = APIRouter()

    def driver() -> ISwitchV3:
        drv = ascom_config.get_driver_instance("switch", device_number)
        if drv is None:
            raise HTTPException(status_code=404, detail="Switch driver not found")
        return drv

    @router.get("/connected")
    def get_connected():
        return make_response(driver().Connected)

    @router.put("/connected")
    def put_connected(value: bool):
        drv = driver()
        drv.Connected = value
        return make_response(drv.Connected)

    @router.get("/description")
    def get_description():
        return make_response(driver().Description)

    @router.get("/driverinfo")
    def get_driverinfo():
        return make_response(driver().DriverInfo)

    @router.get("/driverversion")
    def get_driverversion():
        return make_response(driver().DriverVersion)

    @router.get("/interfaceversion")
    def get_interfaceversion():
        return make_response(driver().InterfaceVersion)

    @router.get("/name")
    def get_name():
        return make_response(driver().Name)

    @router.get("/maxswitch")
    def get_maxswitch():
        return make_response(driver().MaxSwitch)

    @router.get("/getswitchname/{id}")
    def get_switch_name(id: int):
        try:
            return make_response(driver().GetSwitchName(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.put("/setswitchname/{id}")
    def set_switch_name(id: int, name: str):
        try:
            driver().SetSwitchName(id, name)
            return make_response(name)
        except NotImplementedError:
            raise HTTPException(
                status_code=400, detail=make_error("Setting name not supported")
            )
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.get("/getswitchdescription/{id}")
    def get_switch_description(id: int):
        try:
            return make_response(driver().GetSwitchDescription(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.get("/canwrite/{id}")
    def get_canwrite(id: int):
        try:
            return make_response(driver().CanWrite(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.get("/getswitch/{id}")
    def get_switch(id: int):
        try:
            return make_response(driver().GetSwitch(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.put("/setswitch/{id}")
    def set_switch(id: int, state: bool):
        try:
            driver().SetSwitch(id, state)
            return make_response(state)
        except NotImplementedError:
            raise HTTPException(
                status_code=400, detail=make_error("Switch is read-only")
            )
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.get("/getswitchvalue/{id}")
    def get_switch_value(id: int):
        try:
            return make_response(driver().GetSwitchValue(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.put("/setswitchvalue/{id}")
    def set_switch_value(id: int, value: float):
        try:
            driver().SetSwitchValue(id, value)
            return make_response(value)
        except NotImplementedError:
            raise HTTPException(
                status_code=400, detail=make_error("Switch is read-only")
            )
        except ValueError:
            raise HTTPException(
                status_code=400, detail=make_error("Invalid switch value")
            )
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.get("/maxswitchvalue/{id}")
    def get_maxswitchvalue(id: int):
        try:
            return make_response(driver().MaxSwitchValue(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.get("/minswitchvalue/{id}")
    def get_minswitchvalue(id: int):
        try:
            return make_response(driver().MinSwitchValue(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    @router.get("/switchstep/{id}")
    def get_switchstep(id: int):
        try:
            return make_response(driver().SwitchStep(id))
        except Exception:
            raise HTTPException(status_code=400, detail=make_error("Invalid switch id"))

    return router
