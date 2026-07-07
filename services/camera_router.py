from fastapi import APIRouter, HTTPException

from services.config import ascom_config


def get_camera_router(device_number: int):
    device_type = "camera"
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

    @router.get("/devicestate")
    async def devicestate():
        return call_driver("DeviceState")

    @router.put("/startexposure")
    async def start_exposure(Duration: float, Light: bool):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.StartExposure(Duration, Light)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": True,
        }

    @router.put("/stopexposure")
    async def stop_exposure():
        return call_driver("StopExposure")

    @router.put("/abortexposure")
    async def abort_exposure():
        return call_driver("AbortExposure")

    @router.get("/camerastate")
    async def camera_state():
        return call_driver("CameraState")

    @router.get("/imageready")
    async def image_ready():
        return call_driver("ImageReady")

    @router.get("/imagearray")
    async def image_array():
        return call_driver("ImageArray")

    @router.get("/lastexposureduration")
    async def last_exposure_duration():
        return call_driver("LastExposureDuration")

    @router.get("/lastexposurestarttime")
    async def last_exposure_start_time():
        return call_driver("LastExposureStartTime")

    @router.get("/binx")
    async def get_binx():
        return call_driver("BinX")

    @router.put("/binx")
    async def set_binx(BinX: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.BinX = BinX
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": BinX,
        }

    @router.get("/biny")
    async def get_biny():
        return call_driver("BinY")

    @router.put("/biny")
    async def set_biny(BinY: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.BinY = BinY
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": BinY,
        }

    @router.get("/numx")
    async def get_numx():
        return call_driver("NumX")

    @router.put("/numx")
    async def set_numx(NumX: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.NumX = NumX
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": NumX,
        }

    @router.get("/numy")
    async def get_numy():
        return call_driver("NumY")

    @router.put("/numy")
    async def set_numy(NumY: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.NumY = NumY
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": NumY,
        }

    @router.get("/startx")
    async def get_startx():
        return call_driver("StartX")

    @router.put("/startx")
    async def set_startx(StartX: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.StartX = StartX
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": StartX,
        }

    @router.get("/starty")
    async def get_starty():
        return call_driver("StartY")

    @router.put("/starty")
    async def set_starty(StartY: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.StartY = StartY
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": StartY,
        }

    @router.get("/ccdtemperature")
    async def get_ccd_temperature():
        return call_driver("CCDTemperature")

    @router.get("/cooleron")
    async def get_cooler_on():
        return call_driver("CoolerOn")

    @router.put("/cooleron")
    async def set_cooler_on(CoolerOn: bool):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.CoolerOn = CoolerOn
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": CoolerOn,
        }

    @router.get("/setccdtemperature")
    async def get_setccdtemperature():
        return call_driver("SetCCDTemperature")

    @router.put("/setccdtemperature")
    async def set_setccdtemperature(SetCCDTemperature: float):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.SetCCDTemperature = SetCCDTemperature
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": SetCCDTemperature,
        }

    @router.get("/gain")
    async def get_gain():
        return call_driver("Gain")

    @router.put("/gain")
    async def set_gain(Gain: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.Gain = Gain
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": Gain,
        }

    @router.get("/offset")
    async def get_offset():
        return call_driver("Offset")

    @router.put("/offset")
    async def set_offset(Offset: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.Offset = Offset
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": Offset,
        }

    @router.get("/readoutmode")
    async def get_readout_mode():
        return call_driver("ReadoutMode")

    @router.put("/readoutmode")
    async def set_readout_mode(ReadoutMode: int):
        try:
            driver = ascom_config.get_driver_instance(device_type, device_number)
            driver.ReadoutMode = ReadoutMode
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": 0,
            "ErrorNumber": 0,
            "ErrorMessage": "",
            "Value": ReadoutMode,
        }

    return router
