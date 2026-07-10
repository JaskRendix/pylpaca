import pytest

from ASCOMDriver.MyRotatorDriverV4 import MyRotatorDriverV4


@pytest.fixture
def rot():
    r = MyRotatorDriverV4()
    r.Connect()
    return r


def test_connect_disconnect():
    r = MyRotatorDriverV4()
    assert r.Connected is False

    r.Connect()
    assert r.Connected is True

    r.Disconnect()
    assert r.Connected is False


def test_metadata(rot):
    assert rot.InterfaceVersion == 4
    assert isinstance(rot.Description, str)
    assert isinstance(rot.DriverInfo, str)
    assert isinstance(rot.DriverVersion, str)
    assert isinstance(rot.Name, str)


def test_move_relative(rot):
    start_mech = rot.MechanicalPosition
    rot.Move(10.0)

    assert rot.IsMoving is False
    assert rot.MechanicalPosition == (start_mech + 10.0) % 360
    assert rot.TargetPosition == (rot.Position) % 360


def test_move_absolute(rot):
    rot.Sync(0)  # ensure offset = 0
    rot.MoveAbsolute(123.0)

    assert rot.IsMoving is False
    assert rot.Position == pytest.approx(123.0)
    assert rot.MechanicalPosition == pytest.approx(123.0)
    assert rot.TargetPosition == pytest.approx(123.0)


def test_sync(rot):
    rot.MoveMechanical(50.0)
    rot.Sync(80.0)

    # offset = desired - mechanical = 80 - 50 = 30
    assert rot.Position == pytest.approx(80.0)
    assert rot.MechanicalPosition == pytest.approx(50.0)

    # Now absolute move should respect offset
    rot.MoveAbsolute(10.0)
    assert rot.Position == pytest.approx(10.0)
    assert rot.MechanicalPosition == pytest.approx((10.0 - 30.0) % 360)


def test_move_mechanical(rot):
    rot.Sync(100.0)
    rot.MoveMechanical(45.0)

    assert rot.MechanicalPosition == pytest.approx(45.0)
    assert rot.Position == pytest.approx((45.0 + rot._sync_offset) % 360)
    assert rot.TargetPosition == rot.Position


def test_reverse_flag(rot):
    assert rot.Reverse is False
    rot.Reverse = True
    assert rot.Reverse is True


def test_step_size(rot):
    assert rot.StepSize == 0.1


def test_target_position(rot):
    rot.Move(25.0)
    assert rot.TargetPosition == pytest.approx(rot.Position)

    rot.MoveAbsolute(200.0)
    assert rot.TargetPosition == pytest.approx(200.0)


def test_not_connected_errors():
    r = MyRotatorDriverV4()
    with pytest.raises(Exception):
        r.Move(10)

    with pytest.raises(Exception):
        r.MoveAbsolute(10)

    with pytest.raises(Exception):
        r.Sync(10)

    with pytest.raises(Exception):
        r.MoveMechanical(10)


def test_deprecated_commands(rot):
    with pytest.raises(NotImplementedError):
        rot.CommandBlind("X")

    with pytest.raises(NotImplementedError):
        rot.CommandBool("X")

    with pytest.raises(NotImplementedError):
        rot.CommandString("X")


def test_actions(rot):
    assert rot.SupportedActions == []
    with pytest.raises(NotImplementedError):
        rot.Action("Test", "")
