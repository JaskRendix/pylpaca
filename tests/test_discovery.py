import asyncio
import os
import socket

import httpx
import pytest
import uvicorn

from pylpaca.server import AlpacaDiscoveryProtocol, app, get_runtime_settings


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,expected,port",
    [
        (b"alpacaidiscovery1", '{"AlpacaPort": 11111}', 11111),
        (b"", None, 11111),
        (b"\x00\x01\x02\x03", None, 11111),
        (os.urandom(128), None, 11111),
        ("你好世界".encode("utf-16"), None, 11111),
    ],
)
async def test_discovery_protocol_parametrized(payload, expected, port):
    """
    Tests valid, empty, malformed, oversized, and unicode packets.
    """
    loop = asyncio.get_running_loop()
    received = []

    class Client(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            received.append(data.decode("utf-8", errors="ignore"))

    transport_client, _ = await loop.create_datagram_endpoint(
        lambda: Client(), local_addr=("127.0.0.1", 0)
    )

    transport_server, _ = await loop.create_datagram_endpoint(
        lambda: AlpacaDiscoveryProtocol(alpaca_port=port),
        local_addr=("127.0.0.1", 0),
    )

    addr = transport_server.get_extra_info("sockname")
    transport_client.sendto(payload, addr)

    await asyncio.sleep(0.05)

    transport_client.close()
    transport_server.close()

    if expected is None:
        assert received == []
    else:
        assert received[0] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("target", ["127.0.0.1", "255.255.255.255"])
async def test_discovery_protocol_unicast_and_broadcast(target):
    """
    Broadcast may not loop back on Linux; unicast always works.
    """
    loop = asyncio.get_running_loop()
    received = []

    class Client(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            received.append(data.decode("utf-8"))

    transport_client, _ = await loop.create_datagram_endpoint(
        lambda: Client(), local_addr=("127.0.0.1", 0)
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 32227))

    transport_server, _ = await loop.create_datagram_endpoint(
        lambda: AlpacaDiscoveryProtocol(alpaca_port=11111),
        sock=sock,
    )

    transport_client.sendto(b"alpacaidiscovery1", (target, 32227))
    await asyncio.sleep(0.1)

    transport_client.close()
    transport_server.close()

    if target == "127.0.0.1":
        assert received[0] == '{"AlpacaPort": 11111}'


@pytest.mark.asyncio
@pytest.mark.parametrize("port", [12345, 15000])
async def test_full_server_with_discovery_parametrized(tmp_path, port):
    """
    Full FastAPI + Uvicorn + Discovery integration test.
    """
    config_file = tmp_path / "config.json"
    config_file.write_text('{"drivers": []}')

    os.environ["PYLPACA_CONFIG_PATH"] = str(config_file)
    os.environ["PYLPACA_PORT"] = str(port)

    _, host, _ = get_runtime_settings()

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
        for _ in range(50):  # 50 × 20ms = 1 second max
            try:
                r = await client.get(f"http://{host}:{port}/management/apiversions")
                if r.status_code == 200:
                    break
            except httpx.ConnectError:
                await asyncio.sleep(0.02)
        else:
            raise AssertionError("Server did not start in time")

    # UDP test
    loop = asyncio.get_running_loop()
    received = []

    class Client(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            received.append(data.decode("utf-8"))

    transport_client, _ = await loop.create_datagram_endpoint(
        lambda: Client(), local_addr=("127.0.0.1", 0)
    )

    transport_client.sendto(b"alpacaidiscovery1", ("127.0.0.1", 32227))
    await asyncio.sleep(0.1)

    transport_client.close()

    assert received[0] == f'{{"AlpacaPort": {port}}}'

    server.should_exit = True
    await asyncio.sleep(0.2)
    server_task.cancel()


@pytest.mark.asyncio
async def test_discovery_protocol_stress_100_packets():
    """
    Sends 100 discovery packets at a realistic rate.
    Ensures no packet loss under normal Alpaca usage.
    """
    loop = asyncio.get_running_loop()
    received = 0

    class Client(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            nonlocal received
            received += 1

    transport_client, _ = await loop.create_datagram_endpoint(
        lambda: Client(), local_addr=("127.0.0.1", 0)
    )

    transport_server, _ = await loop.create_datagram_endpoint(
        lambda: AlpacaDiscoveryProtocol(alpaca_port=99999),
        local_addr=("127.0.0.1", 0),
    )

    addr = transport_server.get_extra_info("sockname")

    async def send_packet():
        transport_client.sendto(b"alpacaidiscovery1", addr)
        await asyncio.sleep(0)  # yield to event loop

    await asyncio.gather(*(send_packet() for _ in range(100)))

    await asyncio.sleep(0.2)

    transport_client.close()
    transport_server.close()

    assert received == 100
