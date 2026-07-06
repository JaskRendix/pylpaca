import pytest
from pydantic import ValidationError

from services.config import ascom_config
from services.models import AscomConfigModel, DriverConfig


def test_config_loaded():
    cfgs = ascom_config.all_driver_configs()
    assert len(cfgs) >= 1
    assert cfgs[0]["device_type"] == "dome"


@pytest.mark.parametrize(
    "dtype,dnum,expected",
    [
        ("dome", 0, True),
        ("dome", 1, False),
        ("telescope", 0, False),
    ],
)
def test_get_driver_config(dtype, dnum, expected):
    cfg = ascom_config.get_driver_config(dtype, dnum)
    assert (cfg is not None) == expected


def test_invalid_device_type():
    cfg = ascom_config.get_driver_config("invalid_type", 0)
    assert cfg is None


def test_invalid_device_number():
    cfg = ascom_config.get_driver_config("dome", 999)
    assert cfg is None


def test_driver_config_dict_behavior():
    cfg = ascom_config.get_driver_config("dome", 0)
    assert cfg["device_type"] == cfg.device_type
    assert cfg["device_number"] == cfg.device_number


def test_duplicate_device_numbers_rejected():
    # Build a fake config with duplicates
    duplicate = [
        DriverConfig(
            device_type="dome",
            device_number=0,
            device_driver="ASCOMDriver.MyDomeDriver",
        ),
        DriverConfig(
            device_type="dome",
            device_number=0,
            device_driver="ASCOMDriver.MyDomeDriver",
        ),
    ]

    with pytest.raises(ValueError):
        AscomConfigModel(drivers=duplicate)


def test_missing_required_fields():
    with pytest.raises(ValidationError):
        DriverConfig(device_type="dome", device_number=0)  # missing driver_driver


def test_malformed_driver_config():
    with pytest.raises(ValidationError):
        DriverConfig(
            device_type="dome",
            device_number=0,
            device_driver="ASCOMDriver.MyDomeDriver",
            driver_config="not a dict",
        )
