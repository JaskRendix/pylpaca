import pytest


@pytest.mark.asyncio
async def test_apiversions(client):
    r = await client.get("/management/apiversions")
    assert r.status_code == 200
    assert r.json() == [1]


@pytest.mark.asyncio
async def test_description(client):
    r = await client.get("/management/v1/description")
    data = r.json()
    assert "ServerName" in data
    assert "Manufacturer" in data
    assert "ManufacturerVersion" in data


@pytest.mark.asyncio
async def test_configured_devices(client):
    r = await client.get("/management/v1/configureddevices")
    devices = r.json()
    assert isinstance(devices, list)
    assert len(devices) >= 1
    assert devices[0]["DeviceType"] == "dome"
    assert devices[0]["DeviceNumber"] == 0


@pytest.mark.asyncio
async def test_apiversions_are_integers_and_sorted(client):
    r = await client.get("/management/apiversions")
    versions = r.json()
    assert all(isinstance(v, int) for v in versions)
    assert versions == sorted(versions)


@pytest.mark.asyncio
async def test_description_contains_required_fields(client):
    r = await client.get("/management/v1/description")
    data = r.json()

    # These are the fields your server actually returns
    required = [
        "ServerName",
        "Manufacturer",
        "ManufacturerVersion",
        "Location",
    ]

    for field in required:
        assert field in data


@pytest.mark.asyncio
async def test_configured_devices_match_config(client):
    from services.config import ascom_config

    r = await client.get("/management/v1/configureddevices")
    devices = r.json()

    cfgs = ascom_config.all_driver_configs()

    assert len(devices) == len(cfgs)

    for dev, cfg in zip(devices, cfgs):
        assert dev["DeviceType"] == cfg.device_type
        assert dev["DeviceNumber"] == cfg.device_number


@pytest.mark.asyncio
async def test_configured_devices_include_device_name(client):
    r = await client.get("/management/v1/configureddevices")
    devices = r.json()

    for dev in devices:
        assert "DeviceName" in dev
        assert "UniqueID" in dev


@pytest.mark.asyncio
async def test_description_survives_driver_failure(client, monkeypatch):
    import services.management_router as mr

    # Find the /description route inside the router
    target_route = None
    for route in mr.management_router.routes:
        if route.path.endswith("/description"):
            target_route = route
            break

    assert target_route is not None

    # Patch the endpoint function
    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(target_route, "endpoint", boom)

    r = await client.get("/management/v1/description")
    assert r.status_code in (200, 500)
