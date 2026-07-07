import importlib

import uvicorn
from fastapi import FastAPI

from services.config import ascom_config
from services.covercalibrator_router import get_covercalibrator_router
from services.dome_router import get_dome_router
from services.filterwheel_router import get_filterwheel_router
from services.management_router import management_router
from services.telescope_router import get_telescope_router

app = FastAPI(title="Pylpaca FastAPI Server")


def instantiate_driver(cfg) -> None:
    module = importlib.import_module(f"ASCOMDriver.{cfg.device_driver}")
    cls = getattr(module, cfg.device_driver)
    driver = cls(**cfg.driver_config)
    ascom_config.set_driver_instance(cfg.device_type, cfg.device_number, driver)


def register_services() -> None:
    # Management API
    app.include_router(management_router, prefix="/management")

    # Device APIs
    for cfg in ascom_config.all_driver_configs():
        instantiate_driver(cfg)

        if cfg.device_type == "dome":
            router = get_dome_router(cfg.device_number)
            prefix = f"/api/v1/dome/{cfg.device_number}"
            app.include_router(router, prefix=prefix)

        if cfg.device_type == "filterwheel":
            router = get_filterwheel_router(cfg.device_number)
            prefix = f"/api/v1/filterwheel/{cfg.device_number}"
            app.include_router(router, prefix=prefix)

        if cfg.device_type == "telescope":            
            router = get_telescope_router(cfg.device_number)
            prefix = f"/api/v1/telescope/{cfg.device_number}"
            app.include_router(router, prefix=prefix)

        if cfg.device_type == "covercalibrator":            
            router = get_covercalibrator_router(cfg.device_number)
            prefix = f"/api/v1/covercalibrator/{cfg.device_number}"
            app.include_router(router, prefix=prefix)


def get_driver(device_type: str, device_number: int):
    return ascom_config.get_driver_instance(device_type, device_number)


if __name__ == "__main__":
    register_services()
    uvicorn.run(app, host="0.0.0.0", port=11111)
