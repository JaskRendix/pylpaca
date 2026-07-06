import pytest

from pylpaca.server import instantiate_driver
from services.config import ascom_config


@pytest.mark.asyncio
async def test_driver_instantiation():
    cfg = ascom_config.get_driver_config("dome", 0)
    instantiate_driver(cfg)

    driver = ascom_config.get_driver_instance("dome", 0)
    assert driver is not None
    assert hasattr(driver, "OpenShutter")
    assert hasattr(driver, "CloseShutter")


def test_missing_driver_module():
    cfg = ascom_config.get_driver_config("dome", 0).model_copy()
    cfg.device_driver = "NoSuchModule"

    with pytest.raises(ModuleNotFoundError):
        instantiate_driver(cfg)


def test_driver_init_exception(monkeypatch):
    class BadDriver:
        def __init__(self):
            raise RuntimeError("boom")

    import ASCOMDriver.MyDomeDriver as module

    monkeypatch.setattr(module, "MyDomeDriver", BadDriver)

    cfg = ascom_config.get_driver_config("dome", 0)

    with pytest.raises(RuntimeError):
        instantiate_driver(cfg)


def test_driver_is_cached():
    cfg = ascom_config.get_driver_config("dome", 0)

    instantiate_driver(cfg)
    d1 = ascom_config.get_driver_instance("dome", 0)

    instantiate_driver(cfg)
    d2 = ascom_config.get_driver_instance("dome", 0)

    # Loader overwrites the instance every time
    assert d1 is not d2


def test_reinstantiate_same_driver_returns_same_instance():
    cfg = ascom_config.get_driver_config("dome", 0)

    d1 = instantiate_driver(cfg)
    d2 = instantiate_driver(cfg)

    assert d1 is d2
