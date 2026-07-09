import pytest

from ASCOMDriver.MyNWaySwitchDriver import MyNWaySwitchDriver


@pytest.fixture
def driver():
    d = MyNWaySwitchDriver()
    return d


def test_instantiation(driver):
    assert driver.Name == "My NWaySwitch"
    assert driver.DeviceType == "NWaySwitch"
    assert driver.Connected is False


def test_connect_disconnect(driver):
    driver.Connect()
    assert driver.Connected is True
    assert driver.Connecting is False

    driver.Disconnect()
    assert driver.Connected is False
    assert driver.Connecting is False


def test_state(driver):
    driver.Connect()
    state = driver.State
    assert state == ["0", "10", "5"]


def test_set_level(driver):
    driver.Connect()

    driver.SetLevel(7)
    assert driver.State == ["0", "10", "7"]

    with pytest.raises(ValueError):
        driver.SetLevel(-1)

    with pytest.raises(ValueError):
        driver.SetLevel(11)


def test_requires_connection(driver):
    _ = driver.DeviceType
    _ = driver.Name

    with pytest.raises(Exception):
        _ = driver.State

    with pytest.raises(Exception):
        driver.SetLevel(5)


def test_actions(driver):
    driver.Connect()
    assert driver.Action("Test", "") == ""
    assert driver.SupportedActions == []


def test_commands_not_implemented(driver):
    driver.Connect()

    with pytest.raises(NotImplementedError):
        driver.CommandBlind("X")

    with pytest.raises(NotImplementedError):
        driver.CommandBool("X")

    with pytest.raises(NotImplementedError):
        driver.CommandString("X")
