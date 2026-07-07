import pytest

from ASCOMDriver.MyFilterWheelDriver import MyFilterWheelDriver


def test_initial_state_v3():
    d = MyFilterWheelDriver()

    assert d.Connected is False
    assert d.Connecting is False

    assert d.Position == 0
    assert d.Names == ["Luminance", "Red", "Green", "Blue", "Ha"]
    assert d.FocusOffsets == [0, 10, 12, 11, 15]

    assert d.DeviceState == []


def test_connect_workflow_v3():
    d = MyFilterWheelDriver()

    d.Connect()

    assert d.Connected is True
    assert d.Connecting is False


def test_disconnect_workflow_v3():
    d = MyFilterWheelDriver()

    d.Connect()
    assert d.Connected is True

    d.Disconnect()
    assert d.Connected is False
    assert d.Connecting is False


def test_position_setter_v3():
    d = MyFilterWheelDriver()
    d.Connect()

    d.Position = 2
    assert d.Position == 2


def test_position_invalid_v3():
    d = MyFilterWheelDriver()
    d.Connect()

    with pytest.raises(ValueError):
        d.Position = -1

    with pytest.raises(ValueError):
        d.Position = 999


def test_focus_offsets_v3():
    d = MyFilterWheelDriver()
    d.Connect()

    assert d.FocusOffsets == [0, 10, 12, 11, 15]


def test_names_v3():
    d = MyFilterWheelDriver()
    d.Connect()

    assert d.Names == ["Luminance", "Red", "Green", "Blue", "Ha"]


def test_check_connected_enforced_v3():
    d = MyFilterWheelDriver()

    with pytest.raises(Exception):
        _ = d.Position

    with pytest.raises(Exception):
        _ = d.Names

    with pytest.raises(Exception):
        d.Position = 1


def test_action_returns_empty_string_v3():
    d = MyFilterWheelDriver()
    d.Connect()

    assert d.Action("foo", "bar") == ""


def test_supported_actions_is_list_v3():
    d = MyFilterWheelDriver()
    assert isinstance(d.SupportedActions, list)


def test_logging_on_position_change_v3(monkeypatch):
    d = MyFilterWheelDriver()
    d.Connect()

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.Position = 3
    assert called["logged"] is True


def test_no_log_on_same_position_v3(monkeypatch):
    d = MyFilterWheelDriver()
    d.Connect()

    d.Position = 2  # set once

    called = {"logged": False}

    def fake_log(msg):
        called["logged"] = True

    monkeypatch.setattr(d.logger, "info", fake_log)

    d.Position = 2  # no-op
    assert called["logged"] is False
