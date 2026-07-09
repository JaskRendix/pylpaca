# services/video_router.py

from fastapi import APIRouter, HTTPException

from ASCOMDriver.DeviceInterfaces.IVideoV2 import IVideoV2
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


def get_video_router(device_number: int) -> APIRouter:
    router = APIRouter()

    def driver() -> IVideoV2:
        drv = ascom_config.get_driver_instance("video", device_number)
        if drv is None:
            raise HTTPException(status_code=404, detail="Video driver not found")
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
                status_code=400, detail=make_error("Action not implemented")
            )

    @router.get("/videocapturedevicename")
    def get_capture_name():
        return make_response(driver().VideoCaptureDeviceName)

    @router.get("/exposuremax")
    def get_exposuremax():
        return make_response(driver().ExposureMax)

    @router.get("/exposuremin")
    def get_exposuremin():
        return make_response(driver().ExposureMin)

    @router.get("/framerate")
    def get_framerate():
        return make_response(driver().FrameRate)

    @router.get("/supportedintegrationrates")
    def get_supported_integration_rates():
        return make_response(driver().SupportedIntegrationRates)

    @router.get("/integrationrate")
    def get_integrationrate():
        return make_response(driver().IntegrationRate)

    @router.put("/integrationrate")
    def put_integrationrate(value: int):
        drv = driver()

        # Explicit validation BEFORE calling the driver
        rates = drv.SupportedIntegrationRates
        if value < 0 or value >= len(rates):
            raise HTTPException(
                status_code=400, detail=make_error("Invalid integration rate")
            )

        drv.IntegrationRate = value
        return make_response(drv.IntegrationRate)

    @router.get("/lastvideoframe")
    def get_lastvideoframe():
        frame = driver().LastVideoFrame
        return make_response(
            {
                "ImageArray": frame.ImageArray,
                "PreviewBitmap": frame.PreviewBitmap,
                "FrameNumber": frame.FrameNumber,
                "ExposureDuration": frame.ExposureDuration,
                "ExposureStartTime": frame.ExposureStartTime,
                "ImageMetadata": frame.ImageMetadata,
            }
        )

    @router.get("/sensorname")
    def get_sensorname():
        return make_response(driver().SensorName)

    @router.get("/sensortype")
    def get_sensortype():
        return make_response(driver().SensorType)

    return router
