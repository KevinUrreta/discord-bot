import os
import socket

import pytest


@pytest.mark.e2e
def test_configured_services_accept_tcp_connections() -> None:
    if os.environ.get("RUN_E2E") != "1":
        pytest.skip("Set RUN_E2E=1 to run deployment smoke tests")

    required = (
        "E2E_POSTGRES_HOST",
        "E2E_POSTGRES_PORT",
        "E2E_LAVALINK_HOST",
        "E2E_LAVALINK_PORT",
    )
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.fail(f"Missing E2E service configuration: {', '.join(missing)}")

    endpoints = (
        (os.environ["E2E_POSTGRES_HOST"], int(os.environ["E2E_POSTGRES_PORT"])),
        (os.environ["E2E_LAVALINK_HOST"], int(os.environ["E2E_LAVALINK_PORT"])),
    )
    for host, port in endpoints:
        with socket.create_connection((host, port), timeout=3):
            pass
