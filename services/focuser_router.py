from fastapi import APIRouter, HTTPException

from ASCOMDriver.DeviceInterfaces.IFocuserV4 import IFocuserV4
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


def get_focuser_router(device_number: int) -> APIRouter:
    router = APIRouter()

    def driver() -> IFocuserV4:
        drv = ascom_config.get_driver_instance("focuser", device_number)
        if drv is None:
            raise HTTPException(status_code=404, detail="Focuser driver not found")
        return drv

    @router.get("/connected")
    def get_connected():
        return make_response(driver().Connected)

    @router.put("/connected")
    def put_connected(value: bool):
        drv = driver()
        drv.Connected = value
        return make_response(drv.Connected)

    @router.put("/connect")
    def put_connect():
        drv = driver()
        drv.Connect()
        return make_response(True)

    @router.put("/disconnect")
    def put_disconnect():
        drv = driver()
        drv.Disconnect()
        return make_response(False)

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

    @router.get("/supportedactions")
    def get_supportedactions():
        return make_response(driver().SupportedActions)

    @router.put("/action/{action_name}")
    def put_action(action_name: str, action_parameters: str = ""):
        drv = driver()
        try:
            result = drv.Action(action_name, action_parameters)
            return make_response(result)
        except NotImplementedError:
            raise HTTPException(
                status_code=400,
                detail=make_error("Action not implemented"),
            )

    @router.get("/ismoving")
    def get_ismoving():
        return make_response(driver().IsMoving)

    @router.put("/halt")
    def put_halt():
        drv = driver()
        drv.Halt()
        return make_response(False)

    @router.put("/move")
    def put_move(value: int):
        drv = driver()
        try:
            drv.Move(value)
            return make_response(drv.Position)
        except Exception as e:
            raise HTTPException(status_code=400, detail=make_error(str(e)))

    @router.get("/position")
    def get_position():
        try:
            return make_response(driver().Position)
        except Exception as e:
            raise HTTPException(status_code=400, detail=make_error(str(e)))

    @router.get("/absolute")
    def get_absolute():
        return make_response(driver().Absolute)

    @router.get("/maxincrement")
    def get_maxincrement():
        return make_response(driver().MaxIncrement)

    @router.get("/maxstep")
    def get_maxstep():
        return make_response(driver().MaxStep)

    @router.get("/stepsize")
    def get_stepsize():
        return make_response(driver().StepSize)

    @router.get("/tempcomp")
    def get_tempcomp():
        return make_response(driver().TempComp)

    @router.put("/tempcomp")
    def put_tempcomp(value: bool):
        drv = driver()
        try:
            drv.TempComp = value
            return make_response(drv.TempComp)
        except Exception as e:
            raise HTTPException(status_code=400, detail=make_error(str(e)))

    @router.get("/tempcompavailable")
    def get_tempcompavailable():
        return make_response(driver().TempCompAvailable)

    @router.get("/temperature")
    def get_temperature():
        return make_response(driver().Temperature)

    return router
