import asyncio
import os
import socket

import httpx
import pytest
import uvicorn

from pylpaca.server import AlpacaDiscoveryProtocol, app, get_runtime_settings


@pytest.mark.asyncio
async def test_discovery_protocol_basic_response():
    """
    Ensures that sending 'alpacaidiscovery1' produces the correct JSON response.
    """
    loop = asyncio.get_running_loop()
    received = []

    class TestClient(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            received.append(data.decode("utf-8"))

    # Bind client to ephemeral port
    transport_client, protocol_client = await loop.create_datagram_endpoint(
        lambda: TestClient(), local_addr=("127.0.0.1", 0)
    )

    # Bind server to ephemeral port (not 32227)
    transport_server, protocol_server = await loop.create_datagram_endpoint(
        lambda: AlpacaDiscoveryProtocol(alpaca_port=11111), local_addr=("127.0.0.1", 0)
    )

    # Send discovery request
    transport_client.sendto(
        b"alpacaidiscovery1", transport_server.get_extra_info("sockname")
    )

    # Allow async loop to process
    await asyncio.sleep(0.05)

    transport_client.close()
    transport_server.close()

    assert received, "No discovery response received"
    assert received[0] == '{"AlpacaPort": 11111}'


@pytest.mark.asyncio
async def test_discovery_protocol_broadcast():
    loop = asyncio.get_running_loop()
    received = []

    class TestClient(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            received.append(data.decode("utf-8"))

    # Client
    transport_client, _ = await loop.create_datagram_endpoint(
        lambda: TestClient(),
        local_addr=("127.0.0.1", 0),
    )

    # Server socket (matches real server behavior)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 32227))

    transport_server, _ = await loop.create_datagram_endpoint(
        lambda: AlpacaDiscoveryProtocol(alpaca_port=11111),
        sock=sock,
    )

    # Use unicast to localhost instead of broadcast to avoid OS loopback issues
    transport_client.sendto(b"alpacaidiscovery1", ("127.0.0.1", 32227))
    await asyncio.sleep(0.1)

    transport_client.close()
    transport_server.close()

    assert received, "Discovery response not received"
    assert received[0] == '{"AlpacaPort": 11111}'


@pytest.mark.asyncio
async def test_full_server_with_discovery(tmp_path):
    # Temporary config.json
    config_file = tmp_path / "config.json"
    config_file.write_text('{"drivers": []}')

    os.environ["PYLPACA_CONFIG_PATH"] = str(config_file)
    os.environ["PYLPACA_PORT"] = "12345"

    _, host, port = get_runtime_settings()

    # Enable lifespan so discovery + routers load
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="warning",
        lifespan="on",
    )
    server = uvicorn.Server(config)

    server_task = asyncio.create_task(server.serve())
    await asyncio.sleep(0.3)

    # HTTP test
    async with httpx.AsyncClient() as client:
        r = await client.get(f"http://{host}:{port}/management/apiversions")
        assert r.status_code == 200

    # UDP test
    loop = asyncio.get_running_loop()
    received = []

    class TestClient(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            received.append(data.decode("utf-8"))

    transport_client, _ = await loop.create_datagram_endpoint(
        lambda: TestClient(),
        local_addr=("127.0.0.1", 0),
    )

    transport_client.sendto(b"alpacaidiscovery1", ("127.0.0.1", 32227))
    await asyncio.sleep(0.1)

    transport_client.close()

    assert received, "Discovery server did not respond"
    assert received[0] == '{"AlpacaPort": 12345}'

    server.should_exit = True
    await asyncio.sleep(0.2)
    server_task.cancel()


@pytest.mark.asyncio
async def test_discovery_protocol_malformed_packets():
    loop = asyncio.get_running_loop()
    received = []

    class TestClient(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            received.append(data.decode("utf-8"))

    transport_client, protocol_client = await loop.create_datagram_endpoint(
        lambda: TestClient(), local_addr=("127.0.0.1", 0)
    )

    transport_server, protocol_server = await loop.create_datagram_endpoint(
        lambda: AlpacaDiscoveryProtocol(alpaca_port=9999), local_addr=("127.0.0.1", 0)
    )

    # Send garbage
    transport_client.sendto(
        b"\x00\x01\x02\x03", transport_server.get_extra_info("sockname")
    )
    await asyncio.sleep(0.05)

    transport_client.close()
    transport_server.close()

    assert received == [], "Malformed packets should not produce responses"
