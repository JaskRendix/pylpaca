import pytest

from ASCOMDriver.MySwitchDriver import MySwitchDriver


@pytest.fixture
def drv():
    return MySwitchDriver()


def test_connected_property(drv):
    assert drv.Connected is False
    drv.Connected = True
    assert drv.Connected is True


def test_metadata(drv):
    assert drv.Description == "TestSwitch"
    assert drv.DriverInfo.startswith("MySwitchDriver")
    assert drv.DriverVersion == "1.0"
    assert drv.InterfaceVersion == 3
    assert drv.Name == "MySwitchDriver"


def test_maxswitch(drv):
    assert drv.MaxSwitch == 3


def test_get_switch_name_valid(drv):
    assert drv.GetSwitchName(1) == "Switch 1"


def test_get_switch_name_invalid(drv):
    with pytest.raises(ValueError):
        drv.GetSwitchName(99)


def test_set_switch_name_valid(drv):
    drv.SetSwitchName(1, "NewName")
    assert drv.GetSwitchName(1) == "NewName"


def test_set_switch_name_invalid(drv):
    with pytest.raises(ValueError):
        drv.SetSwitchName(99, "X")


def test_get_switch_description_valid(drv):
    assert drv.GetSwitchDescription(2) == "Test switch 2"


def test_get_switch_description_invalid(drv):
    with pytest.raises(ValueError):
        drv.GetSwitchDescription(99)


def test_canwrite_valid(drv):
    assert drv.CanWrite(0) is True


def test_canwrite_invalid(drv):
    with pytest.raises(ValueError):
        drv.CanWrite(99)


def test_getswitch_valid(drv):
    assert drv.GetSwitch(0) is False


def test_getswitch_invalid(drv):
    with pytest.raises(ValueError):
        drv.GetSwitch(99)


def test_setswitch_valid(drv):
    drv.SetSwitch(0, True)
    assert drv.GetSwitch(0) is True
    assert drv.GetSwitchValue(0) == 1.0


def test_setswitch_invalid_id(drv):
    with pytest.raises(ValueError):
        drv.SetSwitch(99, True)


def test_setswitch_readonly(drv):
    drv._can_write[1] = False
    with pytest.raises(NotImplementedError):
        drv.SetSwitch(1, True)


def test_getswitchvalue_valid(drv):
    assert drv.GetSwitchValue(0) == 0.0


def test_getswitchvalue_invalid(drv):
    with pytest.raises(ValueError):
        drv.GetSwitchValue(99)


def test_setswitchvalue_valid(drv):
    drv.SetSwitchValue(0, 1.0)
    assert drv.GetSwitchValue(0) == 1.0
    assert drv.GetSwitch(0) is True


def test_setswitchvalue_invalid_id(drv):
    with pytest.raises(ValueError):
        drv.SetSwitchValue(99, 1.0)


def test_setswitchvalue_invalid_value(drv):
    with pytest.raises(ValueError):
        drv.SetSwitchValue(0, 999)


def test_setswitchvalue_readonly(drv):
    drv._can_write[1] = False
    with pytest.raises(NotImplementedError):
        drv.SetSwitchValue(1, 1.0)


def test_maxswitchvalue(drv):
    assert drv.MaxSwitchValue(0) == 1.0


def test_maxswitchvalue_invalid(drv):
    with pytest.raises(ValueError):
        drv.MaxSwitchValue(99)


def test_minswitchvalue(drv):
    assert drv.MinSwitchValue(0) == 0.0


def test_minswitchvalue_invalid(drv):
    with pytest.raises(ValueError):
        drv.MinSwitchValue(99)


def test_switchstep(drv):
    assert drv.SwitchStep(0) == 1.0


def test_switchstep_invalid(drv):
    with pytest.raises(ValueError):
        drv.SwitchStep(99)


def test_dispose(drv):
    drv.Connected = True
    drv.Dispose()
    assert drv.Connected is False
