from ASCOMDriver.DeviceInterfaces.Enumerations import ShutterState
from ASCOMDriver.MyDomeDriver import MyDomeDriver


def test_initial_shutter_state_v3():
    d = MyDomeDriver()
    assert d.ShutterStatus == ShutterState.shutterClosed


def test_open_shutter_v3(monkeypatch):
    d = MyDomeDriver()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.OpenShutter()

    assert d.ShutterStatus == ShutterState.shutterOpen
    assert called["logged"] is True


def test_close_shutter_v3(monkeypatch):
    d = MyDomeDriver()
    d.OpenShutter()  # open first

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.CloseShutter()

    assert d.ShutterStatus == ShutterState.shutterClosed
    assert called["logged"] is True


def test_shutter_state_changes_correctly_v3():
    d = MyDomeDriver()

    assert d.ShutterStatus == ShutterState.shutterClosed

    d.OpenShutter()
    assert d.ShutterStatus == ShutterState.shutterOpen

    d.CloseShutter()
    assert d.ShutterStatus == ShutterState.shutterClosed


def test_inherits_device_driver_properties_v3():
    d = MyDomeDriver()

    assert d.Name == "MyASCOMDomeDriverV3"
    assert d.Description == "My Dome Driver V3"

    assert d.Connected is False
    d.Connected = True
    assert d.Connected is True


def test_open_shutter_no_op_v3(monkeypatch):
    d = MyDomeDriver()
    d.OpenShutter()  # first open

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.OpenShutter()  # no-op

    assert d.ShutterStatus == ShutterState.shutterOpen
    assert called["logged"] is False


def test_close_shutter_no_op_v3(monkeypatch):
    d = MyDomeDriver()
    d.CloseShutter()  # already closed

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.CloseShutter()  # no-op

    assert d.ShutterStatus == ShutterState.shutterClosed
    assert called["logged"] is False


def test_v3_connect_workflow():
    d = MyDomeDriver()

    assert d.Connecting is False
    assert d.Connected is False

    d.Connect()

    assert d.Connecting is False
    assert d.Connected is True


def test_v3_disconnect_workflow():
    d = MyDomeDriver()

    d.Connect()
    assert d.Connected is True

    d.Disconnect()

    assert d.Connecting is False
    assert d.Connected is False


def test_v3_device_state_collection_exists_and_iterable():
    d = MyDomeDriver()
    state = d.DeviceState

    assert state is not None
    assert hasattr(state, "__iter__")
    assert hasattr(state, "__len__")
    assert hasattr(state, "__getitem__")


def test_v3_metadata():
    d = MyDomeDriver()
    assert d.Name == "MyASCOMDomeDriverV3"
    assert d.Description == "My Dome Driver V3"
