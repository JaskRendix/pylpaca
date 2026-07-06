from fastapi import APIRouter

from services.config import ascom_config

management_router = APIRouter()


@management_router.get("/apiversions")
async def api_versions():
    return [1]


@management_router.get("/v1/description")
async def server_description():
    return {
        "ServerName": "Pylpaca FastAPI Server",
        "Manufacturer": "Pylpaca",
        "ManufacturerVersion": "0.1.0",
        "Location": "Unknown",
    }


@management_router.get("/v1/configureddevices")
async def configured_devices():
    devices = []
    for cfg in ascom_config.all_driver_configs():
        devices.append(
            {
                "DeviceType": cfg.device_type,
                "DeviceNumber": cfg.device_number,
                "DeviceName": cfg.device_driver,
                "UniqueID": f"{cfg.device_type}-{cfg.device_number}",
            }
        )
    return devices
