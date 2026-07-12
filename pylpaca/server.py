import asyncio
import importlib
import os
import socket
from collections.abc import Callable
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

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


class AlpacaDiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self, alpaca_port: int) -> None:
        self.alpaca_port: int = alpaca_port
        self.transport: asyncio.DatagramTransport | None = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport  # type: ignore

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        try:
            msg = data.decode("utf-8", errors="ignore").strip()
            if msg == "alpacaidiscovery1":
                response = f'{{"AlpacaPort": {self.alpaca_port}}}'.encode("utf-8")
                if self.transport:
                    self.transport.sendto(response, addr)
        except Exception:
            pass


def get_runtime_settings() -> tuple[str, str, int]:
    config_path = os.getenv("PYLPACA_CONFIG_PATH", "config.json")
    host = os.getenv("PYLPACA_HOST", "0.0.0.0")
    port = int(os.getenv("PYLPACA_PORT", "11111"))
    return config_path, host, port


app = FastAPI(title="Pylpaca FastAPI Server")

_RETURNED_DRIVER_INSTANCES: dict[tuple[str, int], object] = {}
_SERVICES_REGISTERED: bool = False


@app.exception_handler(HTTPException)
async def alpaca_http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict) and "ErrorNumber" in detail:
        return JSONResponse(status_code=exc.status_code, content=detail)
    if isinstance(detail, str):
        return JSONResponse(
            status_code=exc.status_code,
            content=make_alpaca_error(detail),
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": detail})


def instantiate_driver(cfg) -> object:
    key: tuple[str, int] = (cfg.device_type, cfg.device_number)
    module = importlib.import_module(f"ASCOMDriver.{cfg.device_driver}")
    cls = getattr(module, cfg.device_driver)

    existing = ascom_config._drivers.get(key)

    if existing is not None and type(existing) is cls:
        previous = _RETURNED_DRIVER_INSTANCES.get(key, existing)
        new_driver = cls(**cfg.driver_config)
        ascom_config.set_driver_instance(cfg.device_type, cfg.device_number, new_driver)
        _RETURNED_DRIVER_INSTANCES[key] = previous
        return previous

    new_driver = cls(**cfg.driver_config)
    ascom_config.set_driver_instance(cfg.device_type, cfg.device_number, new_driver)
    _RETURNED_DRIVER_INSTANCES[key] = new_driver
    return new_driver


ROUTER_TABLE: dict[str, Callable[[int], APIRouter]] = {
    "camera": get_camera_router,
    "covercalibrator": get_covercalibrator_router,
    "dome": get_dome_router,
    "filterwheel": get_filterwheel_router,
    "focuser": get_focuser_router,
    "nwayswitch": get_nwayswitch_router,
    "observingconditions": get_observingconditions_router,
    "rotator": get_rotator_router,
    "switch": get_switch_router,
    "telescope": get_telescope_router,
    "video": get_video_router,
}


def register_services() -> None:
    global _SERVICES_REGISTERED
    if _SERVICES_REGISTERED:
        return

    app.include_router(management_router, prefix="/management")

    for cfg in ascom_config.all_driver_configs():
        instantiate_driver(cfg)

        router_factory = ROUTER_TABLE.get(cfg.device_type)
        if router_factory is None:
            raise RuntimeError(f"Unknown device type: {cfg.device_type}")

        router = router_factory(cfg.device_number)
        prefix = f"/api/v1/{cfg.device_type}/{cfg.device_number}"
        app.include_router(router, prefix=prefix)

    _SERVICES_REGISTERED = True


def get_driver(device_type: str, device_number: int) -> object:
    return ascom_config.get_driver_instance(device_type, device_number)


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_services()

    _, _, port = get_runtime_settings()
    loop = asyncio.get_running_loop()

    # Create socket manually for broadcast support
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 32227))

    transport, _ = await loop.create_datagram_endpoint(
        lambda: AlpacaDiscoveryProtocol(alpaca_port=port),
        sock=sock,
    )

    print(f"Alpaca Discovery Server active on UDP 32227 (Announcing port {port})")

    try:
        yield
    finally:
        transport.close()
        print("Alpaca Discovery Server shut down.")


app.router.lifespan_context = lifespan


if __name__ == "__main__":
    register_services()
    _, host, port = get_runtime_settings()
    uvicorn.run(app, host=host, port=port)
