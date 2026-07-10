import pytest

from ASCOMDriver.MyFocuserDriverV4 import MyFocuserDriverV4


@pytest.fixture
def foc():
    f = MyFocuserDriverV4()
    f.Connect()
    return f


def test_connect_disconnect():
    f = MyFocuserDriverV4()
    assert f.Connected is False

    f.Connect()
    assert f.Connected is True

    f.Disconnect()
    assert f.Connected is False


def test_link_property():
    f = MyFocuserDriverV4()
    assert f.Link is False

    f.Link = True
    assert f.Link is True
    assert f.Connected is True

    f.Link = False
    assert f.Link is False
    assert f.Connected is False


def test_metadata(foc):
    assert foc.InterfaceVersion == 4
    assert isinstance(foc.Description, str)
    assert isinstance(foc.DriverInfo, str)
    assert isinstance(foc.DriverVersion, str)
    assert isinstance(foc.Name, str)


def test_absolute_move(foc):
    assert foc.Absolute is True

    foc.Move(100)
    assert foc.Position == 100
    assert foc.IsMoving is False

    foc.Move(0)
    assert foc.Position == 0


def test_absolute_move_out_of_range(foc):
    with pytest.raises(ValueError):
        foc.Move(-1)

    with pytest.raises(ValueError):
        foc.Move(foc.MaxStep + 1)


def test_relative_move():
    f = MyFocuserDriverV4()
    f._absolute = False
    f.Connect()

    start = f._position
    f.Move(50)
    assert f._position == start + 50

    f.Move(-20)
    assert f._position == start + 30


def test_relative_move_out_of_range():
    f = MyFocuserDriverV4()
    f._absolute = False
    f.Connect()

    with pytest.raises(ValueError):
        f.Move(f.MaxIncrement + 1)

    with pytest.raises(ValueError):
        f.Move(-(f.MaxIncrement + 1))


def test_tempcomp_behavior(foc):
    foc.TempComp = True
    foc.Move(10)  # MUST NOT throw
    assert foc.Position == 10

    foc.TempComp = False
    foc.Move(20)
    assert foc.Position == 20


def test_tempcomp_not_available():
    f = MyFocuserDriverV4()
    f._temp_comp_available = False
    f.Connect()

    assert f.TempCompAvailable is False

    with pytest.raises(Exception):
        f.TempComp = True


def test_step_size(foc):
    assert foc.StepSize == 5.0


def test_max_values(foc):
    assert foc.MaxStep == 10000
    assert foc.MaxIncrement == 500


def test_temperature(foc):
    assert isinstance(foc.Temperature, float)


def test_halt(foc):
    foc._is_moving = True
    foc.Halt()
    assert foc.IsMoving is False


def test_not_connected_errors():
    f = MyFocuserDriverV4()

    with pytest.raises(Exception):
        f.Move(10)

    with pytest.raises(Exception):
        _ = f.Position

    # Setting TempComp=False while disconnected is allowed
    f.TempComp = False
    assert f.TempComp is False


def test_deprecated_commands(foc):
    with pytest.raises(NotImplementedError):
        foc.CommandBlind("X")

    with pytest.raises(NotImplementedError):
        foc.CommandBool("X")

    with pytest.raises(NotImplementedError):
        foc.CommandString("X")


def test_actions(foc):
    assert foc.SupportedActions == []
    with pytest.raises(NotImplementedError):
        foc.Action("Test", "")
