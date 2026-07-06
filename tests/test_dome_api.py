import pytest

from ASCOMDriver.DeviceInterfaces.Enumerations import ShutterState


@pytest.mark.asyncio
async def test_shutter_status_initial(client, dome_driver):
    r = await client.get("/api/v1/dome/0/shutterstatus")
    assert r.status_code == 200
    assert r.json()["Value"] == dome_driver.ShutterStatus


@pytest.mark.asyncio
async def test_open_shutter(client, dome_driver):
    await client.put("/api/v1/dome/0/openshutter")
    assert dome_driver.ShutterStatus == ShutterState.shutterOpen


@pytest.mark.asyncio
async def test_close_shutter(client, dome_driver):
    await client.put("/api/v1/dome/0/closeshutter")
    assert dome_driver.ShutterStatus == ShutterState.shutterClosed


@pytest.mark.asyncio
async def test_connected_set_and_get(client, dome_driver):
    # Set connected
    r = await client.put("/api/v1/dome/0/connected?Connected=true")
    assert r.status_code == 200
    assert dome_driver.Connected is True

    # Get connected
    r = await client.get("/api/v1/dome/0/connected")
    assert r.json()["Value"] is True
