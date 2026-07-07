import pytest

from ASCOMDriver.MyDeviceDriver import MyDeviceDriver


def test_initial_state():
    d = MyDeviceDriver("TestName", "TestDescription")
    assert d.Connected is False


def test_connect_sets_state_and_logs(monkeypatch):
    d = MyDeviceDriver("TestName", "TestDescription")

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.Connected = True

    assert d.Connected is True
    assert called["logged"] is True


def test_disconnect_sets_state_and_logs(monkeypatch):
    d = MyDeviceDriver("TestName", "TestDescription")
    d.Connected = True

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.Connected = False

    assert d.Connected is False
    assert called["logged"] is True


def test_setting_same_value_does_not_log(monkeypatch):
    d = MyDeviceDriver("TestName", "TestDescription")

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.Connected = False  # no change

    assert called["logged"] is False


def test_check_connected_raises_when_not_connected():
    d = MyDeviceDriver("TestName", "TestDescription")
    with pytest.raises(ValueError):
        d.CheckConnected("test")


def test_check_connected_passes_when_connected():
    d = MyDeviceDriver("TestName", "TestDescription")
    d.Connected = True
    d.CheckConnected("test")  # should not raise


def test_description_and_name():
    d = MyDeviceDriver("TestName", "TestDescription")
    assert d.Name == "TestName"
    assert d.Description == "TestDescription"


def test_supported_actions_is_list():
    d = MyDeviceDriver("TestName", "TestDescription")
    assert isinstance(d.SupportedActions, list)
    assert d.SupportedActions == []


def test_action_not_implemented():
    d = MyDeviceDriver("TestName", "TestDescription")
    with pytest.raises(NotImplementedError):
        d.Action("foo", "bar")


def test_command_methods_require_connection():
    d = MyDeviceDriver("TestName", "TestDescription")

    with pytest.raises(ValueError):
        d.CommandBlind("X")

    with pytest.raises(ValueError):
        d.CommandBool("X")

    with pytest.raises(ValueError):
        d.CommandString("X")


def test_command_methods_raise_not_implemented_when_connected():
    d = MyDeviceDriver("TestName", "TestDescription")
    d.Connected = True

    with pytest.raises(NotImplementedError):
        d.CommandBlind("X")

    with pytest.raises(NotImplementedError):
        d.CommandBool("X")

    with pytest.raises(NotImplementedError):
        d.CommandString("X")
