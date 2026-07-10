from fastapi import APIRouter, HTTPException

from ASCOMDriver.DeviceInterfaces.IRotatorV4 import IRotatorV4
from services.config import ascom_config
from services.device_router import make_alpaca_error, make_alpaca_response


def get_rotator_router(device_number: int) -> APIRouter:
    router = APIRouter()

    def driver() -> IRotatorV4:
        drv = ascom_config.get_driver_instance("rotator", device_number)
        if drv is None:
            raise HTTPException(status_code=404, detail="Rotator driver not found")
        return drv

    @router.get("/connected")
    def get_connected():
        return make_alpaca_response(driver().Connected)

    @router.put("/connected")
    def put_connected(value: bool):
        drv = driver()
        drv.Connected = value
        return make_alpaca_response(drv.Connected)

    @router.put("/connect")
    def put_connect():
        drv = driver()
        drv.Connect()
        return make_alpaca_response(True)

    @router.put("/disconnect")
    def put_disconnect():
        drv = driver()
        drv.Disconnect()
        return make_alpaca_response(False)

    @router.get("/description")
    def get_description():
        return make_alpaca_response(driver().Description)

    @router.get("/driverinfo")
    def get_driverinfo():
        return make_alpaca_response(driver().DriverInfo)

    @router.get("/driverversion")
    def get_driverversion():
        return make_alpaca_response(driver().DriverVersion)

    @router.get("/interfaceversion")
    def get_interfaceversion():
        return make_alpaca_response(driver().InterfaceVersion)

    @router.get("/name")
    def get_name():
        return make_alpaca_response(driver().Name)

    @router.get("/supportedactions")
    def get_supportedactions():
        return make_alpaca_response(driver().SupportedActions)

    @router.put("/action/{action_name}")
    def put_action(action_name: str, action_parameters: str = ""):
        drv = driver()
        try:
            result = drv.Action(action_name, action_parameters)
            return make_alpaca_response(result)
        except NotImplementedError:
            raise HTTPException(
                status_code=400,
                detail=make_alpaca_error("Action not implemented"),
            )

    @router.get("/ismoving")
    def get_ismoving():
        return make_alpaca_response(driver().IsMoving)

    @router.put("/halt")
    def put_halt():
        drv = driver()
        drv.Halt()
        return make_alpaca_response(False)

    @router.put("/move")
    def put_move(value: float):
        drv = driver()
        try:
            drv.Move(value)
            return make_alpaca_response(drv.TargetPosition)
        except Exception as e:
            raise HTTPException(status_code=400, detail=make_alpaca_error(str(e)))

    @router.put("/moveabsolute")
    def put_moveabsolute(value: float):
        drv = driver()
        try:
            drv.MoveAbsolute(value)
            return make_alpaca_response(drv.TargetPosition)
        except Exception as e:
            raise HTTPException(status_code=400, detail=make_alpaca_error(str(e)))

    @router.put("/movemechanical")
    def put_movemechanical(value: float):
        drv = driver()
        try:
            drv.MoveMechanical(value)
            return make_alpaca_response(drv.MechanicalPosition)
        except Exception as e:
            raise HTTPException(status_code=400, detail=make_alpaca_error(str(e)))

    @router.put("/sync")
    def put_sync(value: float):
        drv = driver()
        try:
            drv.Sync(value)
            return make_alpaca_response(drv.Position)
        except Exception as e:
            raise HTTPException(status_code=400, detail=make_alpaca_error(str(e)))

    @router.get("/position")
    def get_position():
        return make_alpaca_response(driver().Position)

    @router.get("/mechanicalposition")
    def get_mechanicalposition():
        return make_alpaca_response(driver().MechanicalPosition)

    @router.get("/targetposition")
    def get_targetposition():
        return make_alpaca_response(driver().TargetPosition)

    @router.get("/reverse")
    def get_reverse():
        return make_alpaca_response(driver().Reverse)

    @router.put("/reverse")
    def put_reverse(value: bool):
        drv = driver()
        drv.Reverse = value
        return make_alpaca_response(drv.Reverse)

    @router.get("/stepsize")
    def get_stepsize():
        return make_alpaca_response(driver().StepSize)

    return router
