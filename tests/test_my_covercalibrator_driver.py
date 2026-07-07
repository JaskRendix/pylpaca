import pytest

from ASCOMDriver.MyCoverCalibratorDriver import MyCoverCalibratorDriver
from ASCOMDriver.DeviceInterfaces.Enumerations import CoverStatus, CalibratorStatus


def test_initial_state_v2():
    d = MyCoverCalibratorDriver()

    assert d.Connected is False
    assert d.Connecting is False

    assert d.CoverState == CoverStatus.Closed
    assert d.CalibratorState == CalibratorStatus.Off
    assert d.Brightness == 0
    assert d.MaxBrightness == 255


def test_connect_workflow_v2():
    d = MyCoverCalibratorDriver()

    d.Connect()

    assert d.Connected is True
    assert d.Connecting is False


def test_disconnect_workflow_v2():
    d = MyCoverCalibratorDriver()

    d.Connect()
    assert d.Connected is True

    d.Disconnect()
    assert d.Connected is False
    assert d.Connecting is False


def test_cover_operations_v2():
    d = MyCoverCalibratorDriver()
    d.Connect()

    # open
    d.OpenCover()
    assert d.CoverState == CoverStatus.Open

    # close
    d.CloseCover()
    assert d.CoverState == CoverStatus.Closed

    # halt
    d.HaltCover()
    # halt does not change state, only logs
    assert d.CoverState == CoverStatus.Closed


def test_cover_no_op_v2(monkeypatch):
    d = MyCoverCalibratorDriver()
    d.Connect()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    # already closed → no log
    d.CloseCover()
    assert called["logged"] is False

    # open once
    d.OpenCover()
    assert called["logged"] is True

    # reset
    called["logged"] = False

    # open again → no log
    d.OpenCover()
    assert called["logged"] is False


def test_calibrator_operations_v2():
    d = MyCoverCalibratorDriver()
    d.Connect()

    d.CalibratorOn(100)
    assert d.CalibratorState == CalibratorStatus.Ready
    assert d.Brightness == 100

    d.CalibratorOff()
    assert d.CalibratorState == CalibratorStatus.Off
    assert d.Brightness == 0


def test_calibrator_invalid_brightness_v2():
    d = MyCoverCalibratorDriver()
    d.Connect()

    with pytest.raises(ValueError):
        d.CalibratorOn(-1)

    with pytest.raises(ValueError):
        d.CalibratorOn(9999)


def test_check_connected_enforced_v2():
    d = MyCoverCalibratorDriver()

    with pytest.raises(Exception):
        _ = d.CoverState

    with pytest.raises(Exception):
        d.OpenCover()

    with pytest.raises(Exception):
        d.CalibratorOn(10)


def test_action_returns_empty_string_v2():
    d = MyCoverCalibratorDriver()
    d.Connect()

    assert d.Action("foo", "bar") == ""


def test_supported_actions_is_list_v2():
    d = MyCoverCalibratorDriver()
    assert isinstance(d.SupportedActions, list)
