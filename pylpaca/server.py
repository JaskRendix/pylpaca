import importlib

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from services.camera_router import get_camera_router
from services.config import ascom_config
from services.covercalibrator_router import get_covercalibrator_router
from services.device_router import make_alpaca_error
from services.dome_router import get_dome_router
from services.filterwheel_router import get_filterwheel_router
from services.focuser_router import get_focuser_router
from services.management_router import management_router
from services.nwayswitch_router import get_nwayswitch_router
from services.observingconditions_router import get_observingconditions_router
from services.rotator_router import get_rotator_router
from services.switch_router import get_switch_router
from services.telescope_router import get_telescope_router
from services.video_router import get_video_router

app = FastAPI(title="Pylpaca FastAPI Server")

_RETURNED_DRIVER_INSTANCES: dict[tuple[str, int], object] = {}


@app.exception_handler(HTTPException)
async def alpaca_http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict) and "ErrorNumber" in detail:
        return JSONResponse(status_code=exc.status_code, content=detail)
    if isinstance(detail, str):
        return JSONResponse(
            status_code=exc.status_code,
            content=make_alpaca_error(detail),
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": detail})


def instantiate_driver(cfg):
    key = (cfg.device_type, cfg.device_number)
    module = importlib.import_module(f"ASCOMDriver.{cfg.device_driver}")
    cls = getattr(module, cfg.device_driver)

    existing = ascom_config._drivers.get(key)
    if existing is not None and type(existing) is cls:
        previous = _RETURNED_DRIVER_INSTANCES.get(key, existing)
        driver = cls(**cfg.driver_config)
        ascom_config.set_driver_instance(cfg.device_type, cfg.device_number, driver)
        _RETURNED_DRIVER_INSTANCES[key] = previous
        return previous

    driver = cls(**cfg.driver_config)
    ascom_config.set_driver_instance(cfg.device_type, cfg.device_number, driver)
    _RETURNED_DRIVER_INSTANCES[key] = driver
    return driver


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
        elif cfg.device_type == "filterwheel":
            router = get_filterwheel_router(cfg.device_number)
            prefix = f"/api/v1/filterwheel/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "telescope":
            router = get_telescope_router(cfg.device_number)
            prefix = f"/api/v1/telescope/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "covercalibrator":
            router = get_covercalibrator_router(cfg.device_number)
            prefix = f"/api/v1/covercalibrator/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "camera":
            router = get_camera_router(cfg.device_number)
            prefix = f"/api/v1/camera/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "observingconditions":
            router = get_observingconditions_router(cfg.device_number)
            prefix = f"/api/v1/observingconditions/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "nwayswitch":
            router = get_nwayswitch_router(cfg.device_number)
            prefix = f"/api/v1/nwayswitch/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "switch":
            router = get_switch_router(cfg.device_number)
            prefix = f"/api/v1/switch/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "video":
            router = get_video_router(cfg.device_number)
            prefix = f"/api/v1/video/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "focuser":
            router = get_focuser_router(cfg.device_number)
            prefix = f"/api/v1/focuser/{cfg.device_number}"
            app.include_router(router, prefix=prefix)
        elif cfg.device_type == "rotator":
            router = get_rotator_router(cfg.device_number)
            prefix = f"/api/v1/rotator/{cfg.device_number}"
            app.include_router(router, prefix=prefix)


def get_driver(device_type: str, device_number: int):
    return ascom_config.get_driver_instance(device_type, device_number)


if __name__ == "__main__":
    register_services()
    uvicorn.run(app, host="0.0.0.0", port=11111)
