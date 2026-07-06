from ASCOMDriver.DeviceInterfaces.Enumerations import ShutterState
from ASCOMDriver.MyDomeDriver import MyDomeDriver


def test_initial_shutter_state():
    d = MyDomeDriver()
    assert d.ShutterStatus == ShutterState.shutterClosed


def test_open_shutter(monkeypatch):
    d = MyDomeDriver()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.OpenShutter()

    assert d.ShutterStatus == ShutterState.shutterOpen
    assert called["logged"] is True


def test_close_shutter(monkeypatch):
    d = MyDomeDriver()
    d.OpenShutter()  # open first

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.CloseShutter()

    assert d.ShutterStatus == ShutterState.shutterClosed
    assert called["logged"] is True


def test_shutter_state_changes_correctly():
    d = MyDomeDriver()

    # initial
    assert d.ShutterStatus == ShutterState.shutterClosed

    # open
    d.OpenShutter()
    assert d.ShutterStatus == ShutterState.shutterOpen

    # close
    d.CloseShutter()
    assert d.ShutterStatus == ShutterState.shutterClosed


def test_inherits_device_driver_properties():
    d = MyDomeDriver()

    # inherited from MyDeviceDriver
    assert d.Name == "MyASCOMDomeDriver"
    assert d.Description == "My driver description"

    # inherited connection logic
    assert d.Connected is False
    d.Connected = True
    assert d.Connected is True


def test_open_shutter_no_op(monkeypatch):
    d = MyDomeDriver()
    d.OpenShutter()  # first open

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    # second open → no change → no log
    d.OpenShutter()

    assert d.ShutterStatus == ShutterState.shutterOpen
    assert called["logged"] is False


def test_close_shutter_no_op(monkeypatch):
    d = MyDomeDriver()
    d.CloseShutter()  # already closed

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    # second close → no change → no log
    d.CloseShutter()

    assert d.ShutterStatus == ShutterState.shutterClosed
    assert called["logged"] is False
