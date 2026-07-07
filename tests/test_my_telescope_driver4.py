from ASCOMDriver.DeviceInterfaces.Enumerations import (
    AlignmentModes,
    DriveRates,
    EquatorialCoordinateType,
    PierSide,
)
from ASCOMDriver.MyTelescopeDriverV4 import MyTelescopeDriverV4


def test_initial_state_v4():
    t = MyTelescopeDriverV4()

    assert t.Connected is False
    assert t.Connecting is False
    assert t.DeviceState == []

    assert t.RightAscension == 0.0
    assert t.Declination == 0.0
    assert t.Tracking is False
    assert t.TrackingRate == DriveRates.driveSidereal


def test_connect_workflow_v4(monkeypatch):
    t = MyTelescopeDriverV4()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(t.logger, "info", fake_log)

    t.Connect()

    assert t.Connected is True
    assert t.Connecting is False
    assert called["logged"] is True


def test_disconnect_workflow_v4(monkeypatch):
    t = MyTelescopeDriverV4()
    t.Connect()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(t.logger, "info", fake_log)

    t.Disconnect()

    assert t.Connected is False
    assert t.Connecting is False
    assert called["logged"] is True


def test_alignment_mode_v4():
    t = MyTelescopeDriverV4()
    assert t.AlignmentMode == AlignmentModes.algAltAz


def test_equatorial_system_v4():
    t = MyTelescopeDriverV4()
    assert t.EquatorialSystem == EquatorialCoordinateType.equLocalTopocentric


def test_ra_dec_properties_v4():
    t = MyTelescopeDriverV4()

    assert t.RightAscension == 0.0
    assert t.Declination == 0.0


def test_tracking_setter_v4():
    t = MyTelescopeDriverV4()

    assert t.Tracking is False
    t.Tracking = True
    assert t.Tracking is True


def test_tracking_rate_setter_v4():
    t = MyTelescopeDriverV4()

    assert t.TrackingRate == DriveRates.driveSidereal
    t.TrackingRate = DriveRates.driveSolar
    assert t.TrackingRate == DriveRates.driveSolar


def test_capabilities_v4():
    t = MyTelescopeDriverV4()

    assert t.CanSetTracking is True
    assert t.CanFindHome is False
    assert t.CanPark is False
    assert t.CanPulseGuide is False
    assert t.CanSlew is False
    assert t.CanSlewAsync is False
    assert t.CanSync is False
    assert t.CanUnpark is False


def test_side_of_pier_v4():
    t = MyTelescopeDriverV4()
    assert t.SideOfPier == PierSide.pierUnknown


def test_abort_slew_requires_connection_v4():
    t = MyTelescopeDriverV4()

    try:
        t.AbortSlew()
        assert False, "Expected exception"
    except Exception:
        assert True


def test_axis_rates_not_implemented_v4():
    t = MyTelescopeDriverV4()
    t.Connect()

    try:
        t.AxisRates(None)
        assert False
    except NotImplementedError:
        assert True


def test_tracking_rates_not_implemented_v4():
    t = MyTelescopeDriverV4()
    t.Connect()

    try:
        _ = t.TrackingRates
        assert False
    except NotImplementedError:
        assert True
