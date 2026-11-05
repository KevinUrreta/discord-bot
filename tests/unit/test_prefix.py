import asyncio
from types import SimpleNamespace

from src.helpers import prefix


class FakeGuildSettingsRepository:
    def __init__(self, _database: object) -> None:
        pass

    async def read(self, guild_id: int) -> SimpleNamespace | None:
        return SETTINGS_BY_GUILD.get(guild_id)


SETTINGS_BY_GUILD: dict[int, SimpleNamespace] = {}


def test_get_prefix_returns_default_for_direct_messages(monkeypatch) -> None:
    def unexpected_repository(_database: object) -> None:
        raise AssertionError("Direct messages should not query guild settings")

    monkeypatch.setattr(prefix, "GuildSettingsRepository", unexpected_repository)
    message = SimpleNamespace(guild=None)

    assert asyncio.run(prefix.get_prefix(SimpleNamespace(db=None), message)) == "!"


def test_get_prefix_returns_default_when_settings_are_missing(monkeypatch) -> None:
    SETTINGS_BY_GUILD.clear()
    monkeypatch.setattr(prefix, "GuildSettingsRepository", FakeGuildSettingsRepository)
    message = SimpleNamespace(guild=SimpleNamespace(id=123), content="!ping")

    assert asyncio.run(prefix.get_prefix(SimpleNamespace(db=None), message)) == "!"


def test_get_prefix_returns_configured_prefix(monkeypatch) -> None:
    SETTINGS_BY_GUILD.clear()
    SETTINGS_BY_GUILD[123] = SimpleNamespace(prefix="?")
    monkeypatch.setattr(prefix, "GuildSettingsRepository", FakeGuildSettingsRepository)
    message = SimpleNamespace(guild=SimpleNamespace(id=123), content="?ping")

    assert asyncio.run(prefix.get_prefix(SimpleNamespace(db=None), message)) == "?"


def test_get_prefix_ignores_bot_mentions_when_prefix_is_less_than(monkeypatch) -> None:
    SETTINGS_BY_GUILD.clear()
    SETTINGS_BY_GUILD[123] = SimpleNamespace(prefix="<")
    monkeypatch.setattr(prefix, "GuildSettingsRepository", FakeGuildSettingsRepository)
    message = SimpleNamespace(guild=SimpleNamespace(id=123), content="<@456> ping")

    assert asyncio.run(prefix.get_prefix(SimpleNamespace(db=None), message)) == "\0"
