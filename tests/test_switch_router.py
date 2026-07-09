from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from services.config import ascom_config
from services.switch_router import get_switch_router


@pytest.fixture
def mock_driver():
    drv = MagicMock()
    drv.Connected = False
    drv.Description = "TestSwitch"
    drv.DriverInfo = "DriverInfo"
    drv.DriverVersion = "1.0"
    drv.InterfaceVersion = 3
    drv.Name = "MySwitchDriver"

    drv.MaxSwitch = 3
    drv.GetSwitchName.side_effect = lambda i: (
        f"Switch {i}" if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )
    drv.SetSwitchName.side_effect = lambda i, n: (
        None if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )

    drv.GetSwitchDescription.side_effect = lambda i: (
        f"Desc {i}" if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )

    drv.CanWrite.side_effect = lambda i: (
        True if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )

    drv.GetSwitch.side_effect = lambda i: (
        False if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )
    drv.SetSwitch.side_effect = lambda i, s: (
        None if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )

    drv.GetSwitchValue.side_effect = lambda i: (
        0.0 if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )
    drv.SetSwitchValue.side_effect = lambda i, v: (
        None
        if (0 <= i < 3 and 0.0 <= v <= 1.0)
        else (_ for _ in ()).throw(ValueError())
    )

    drv.MaxSwitchValue.side_effect = lambda i: (
        1.0 if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )
    drv.MinSwitchValue.side_effect = lambda i: (
        0.0 if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )
    drv.SwitchStep.side_effect = lambda i: (
        1.0 if 0 <= i < 3 else (_ for _ in ()).throw(ValueError())
    )

    return drv


@pytest.fixture
def client(mock_driver):
    ascom_config.set_driver_instance("switch", 0, mock_driver)
    router = get_switch_router(0)
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router, prefix="/switch/0")
    return TestClient(app)


def test_get_connected(client, mock_driver):
    mock_driver.Connected = True
    r = client.get("/switch/0/connected")
    assert r.status_code == 200
    assert r.json()["Value"] is True


def test_put_connected(client, mock_driver):
    r = client.put("/switch/0/connected", params={"value": True})
    assert r.status_code == 200
    assert mock_driver.Connected is True


def test_metadata(client):
    assert client.get("/switch/0/description").json()["Value"] == "TestSwitch"
    assert client.get("/switch/0/driverinfo").json()["Value"] == "DriverInfo"
    assert client.get("/switch/0/driverversion").json()["Value"] == "1.0"
    assert client.get("/switch/0/interfaceversion").json()["Value"] == 3
    assert client.get("/switch/0/name").json()["Value"] == "MySwitchDriver"


def test_maxswitch(client):
    r = client.get("/switch/0/maxswitch")
    assert r.json()["Value"] == 3


def test_get_switch_name_valid(client):
    r = client.get("/switch/0/getswitchname/1")
    assert r.json()["Value"] == "Switch 1"


def test_get_switch_name_invalid(client):
    r = client.get("/switch/0/getswitchname/99")
    assert r.status_code == 400


def test_set_switch_name_valid(client):
    r = client.put("/switch/0/setswitchname/1", params={"name": "NewName"})
    assert r.status_code == 200


def test_set_switch_name_invalid(client):
    r = client.put("/switch/0/setswitchname/99", params={"name": "X"})
    assert r.status_code == 400


def test_get_switch_description_valid(client):
    r = client.get("/switch/0/getswitchdescription/2")
    assert r.json()["Value"] == "Desc 2"


def test_get_switch_description_invalid(client):
    r = client.get("/switch/0/getswitchdescription/99")
    assert r.status_code == 400


def test_canwrite_valid(client):
    r = client.get("/switch/0/canwrite/1")
    assert r.json()["Value"] is True


def test_canwrite_invalid(client):
    r = client.get("/switch/0/canwrite/99")
    assert r.status_code == 400


def test_getswitch_valid(client):
    r = client.get("/switch/0/getswitch/0")
    assert r.json()["Value"] is False


def test_getswitch_invalid(client):
    r = client.get("/switch/0/getswitch/99")
    assert r.status_code == 400


def test_setswitch_valid(client):
    r = client.put("/switch/0/setswitch/0", params={"state": True})
    assert r.status_code == 200


def test_setswitch_invalid_id(client):
    r = client.put("/switch/0/setswitch/99", params={"state": True})
    assert r.status_code == 400


def test_getswitchvalue_valid(client):
    r = client.get("/switch/0/getswitchvalue/0")
    assert r.json()["Value"] == 0.0


def test_getswitchvalue_invalid(client):
    r = client.get("/switch/0/getswitchvalue/99")
    assert r.status_code == 400


def test_setswitchvalue_valid(client):
    r = client.put("/switch/0/setswitchvalue/0", params={"value": 1.0})
    assert r.status_code == 200


def test_setswitchvalue_invalid_id(client):
    r = client.put("/switch/0/setswitchvalue/99", params={"value": 1.0})
    assert r.status_code == 400


def test_setswitchvalue_invalid_value(client):
    r = client.put("/switch/0/setswitchvalue/0", params={"value": 999})
    assert r.status_code == 400


def test_maxswitchvalue_valid(client):
    r = client.get("/switch/0/maxswitchvalue/0")
    assert r.json()["Value"] == 1.0


def test_maxswitchvalue_invalid(client):
    r = client.get("/switch/0/maxswitchvalue/99")
    assert r.status_code == 400


def test_minswitchvalue_valid(client):
    r = client.get("/switch/0/minswitchvalue/0")
    assert r.json()["Value"] == 0.0


def test_minswitchvalue_invalid(client):
    r = client.get("/switch/0/minswitchvalue/99")
    assert r.status_code == 400


def test_switchstep_valid(client):
    r = client.get("/switch/0/switchstep/0")
    assert r.json()["Value"] == 1.0


def test_switchstep_invalid(client):
    r = client.get("/switch/0/switchstep/99")
    assert r.status_code == 400
