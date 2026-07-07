from ASCOMDriver.DeviceInterfaces.Enumerations import (
    AlignmentModes,
    DriveRates,
    EquatorialCoordinateType,
    PierSide,
)
from ASCOMDriver.MyTelescopeDriverV3 import MyTelescopeDriverV3


def test_initial_state():
    t = MyTelescopeDriverV3()

    assert t.Connected is False
    assert t.Connecting is False
    assert t.DeviceState == []

    assert t.RightAscension == 0.0
    assert t.Declination == 0.0
    assert t.Tracking is False
    assert t.TrackingRate == DriveRates.driveSidereal


def test_connect_workflow(monkeypatch):
    t = MyTelescopeDriverV3()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(t.logger, "info", fake_log)

    t.Connect()

    assert t.Connected is True
    assert t.Connecting is False
    assert called["logged"] is True


def test_disconnect_workflow(monkeypatch):
    t = MyTelescopeDriverV3()
    t.Connect()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(t.logger, "info", fake_log)

    t.Disconnect()

    assert t.Connected is False
    assert t.Connecting is False
    assert called["logged"] is True


def test_alignment_mode():
    t = MyTelescopeDriverV3()
    assert t.AlignmentMode == AlignmentModes.algAltAz


def test_equatorial_system():
    t = MyTelescopeDriverV3()
    assert t.EquatorialSystem == EquatorialCoordinateType.equLocalTopocentric


def test_ra_dec_properties():
    t = MyTelescopeDriverV3()

    assert t.RightAscension == 0.0
    assert t.Declination == 0.0


def test_tracking_setter():
    t = MyTelescopeDriverV3()

    assert t.Tracking is False
    t.Tracking = True
    assert t.Tracking is True


def test_tracking_rate_setter():
    t = MyTelescopeDriverV3()

    assert t.TrackingRate == DriveRates.driveSidereal
    t.TrackingRate = DriveRates.driveSolar
    assert t.TrackingRate == DriveRates.driveSolar


def test_capabilities():
    t = MyTelescopeDriverV3()

    assert t.CanSetTracking is True
    assert t.CanFindHome is False
    assert t.CanPark is False
    assert t.CanPulseGuide is False
    assert t.CanSlew is False
    assert t.CanSlewAsync is False
    assert t.CanSync is False
    assert t.CanUnpark is False


def test_side_of_pier():
    t = MyTelescopeDriverV3()
    assert t.SideOfPier == PierSide.pierUnknown


def test_abort_slew_requires_connection():
    t = MyTelescopeDriverV3()

    try:
        t.AbortSlew()
        assert False, "Expected exception"
    except Exception:
        assert True


def test_command_methods_raise(monkeypatch):
    t = MyTelescopeDriverV3()
    t.Connect()

    # AxisRates is intentionally unimplemented
    try:
        t.AxisRates(None)
        assert False
    except NotImplementedError:
        assert True

    # TrackingRates is intentionally unimplemented
    try:
        _ = t.TrackingRates
        assert False
    except NotImplementedError:
        assert True
