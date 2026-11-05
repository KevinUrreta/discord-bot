import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

from src.app.commands.info.ping import Ping


def test_ping_sends_localized_latency_embed():
    context = SimpleNamespace(
        author=SimpleNamespace(
            display_name="Test user",
            display_avatar=SimpleNamespace(url="https://example.test/avatar.png"),
        ),
        send=AsyncMock(),
    )
    command = Ping(client=SimpleNamespace(latency=0.052))

    asyncio.run(Ping.ping.callback(command, context))

    context.send.assert_awaited_once()
    embed = context.send.await_args.kwargs["embed"]
    assert embed.title == "Pong!"
    assert embed.description == "Current latency: **52 ms**."
    assert embed.footer.text == "Requested by: Test user"
