import pytest

from ASCOMDriver.MyObservingConditionsDriver import MyObservingConditionsDriver


@pytest.fixture
def driver():
    d = MyObservingConditionsDriver()
    return d


def test_instantiation(driver):
    assert driver.Name == "My ObservingConditions Driver V2"
    assert driver.InterfaceVersion == 2
    assert driver.Connected is False


def test_connect_disconnect(driver):
    driver.Connect()
    assert driver.Connected is True
    assert driver.Connecting is False

    driver.Disconnect()
    assert driver.Connected is False
    assert driver.Connecting is False


def test_average_period(driver):
    driver.Connect()
    driver.AveragePeriod = 0.0
    assert driver.AveragePeriod == 0.0

    driver.AveragePeriod = 1.5
    assert driver.AveragePeriod == 1.5

    with pytest.raises(ValueError):
        driver.AveragePeriod = -1


def test_environment_properties(driver):
    driver.Connect()

    assert isinstance(driver.CloudCover, float)
    assert isinstance(driver.DewPoint, float)
    assert isinstance(driver.Humidity, float)
    assert isinstance(driver.Pressure, float)
    assert isinstance(driver.RainRate, float)
    assert isinstance(driver.SkyBrightness, float)


def test_v2_properties(driver):
    driver.Connect()

    assert isinstance(driver.SkyQuality, float)
    assert isinstance(driver.StarFWHM, float)
    assert isinstance(driver.SkyTemperature, float)
    assert isinstance(driver.Temperature, float)


def test_requires_connection(driver):
    with pytest.raises(Exception):
        _ = driver.CloudCover

    with pytest.raises(Exception):
        _ = driver.SkyQuality

    with pytest.raises(Exception):
        driver.AveragePeriod = 1.0


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
