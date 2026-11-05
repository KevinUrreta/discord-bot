import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import wavelink

from src.app.commands.info.prefix import Prefix
from src.app.commands.music.autoplay import AutoplayCommand
from src.app.commands.music.volume import Volume
from src.app.commands.settings.language import Language
from src.helpers.embed import CustomEmbed


async def make_embed(*args, **kwargs):
    return "test embed"


def make_context(player=None):
    user = SimpleNamespace(
        display_name="Test user",
        display_avatar=SimpleNamespace(url="https://example.test/avatar.png"),
    )
    return SimpleNamespace(
        author=user,
        guild=SimpleNamespace(id=123),
        voice_client=player,
        send=AsyncMock(),
    )


def test_prefix_saves_new_value(monkeypatch):
    from src.app.commands.info import prefix as prefix_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(prefix="!")

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(prefix_module, "GuildSettingsRepository", SettingsRepository)
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    command = Prefix(SimpleNamespace(db=None))

    asyncio.run(Prefix.prefix.callback(command, context, "?"))

    assert updates == [(123, {"prefix": "?"})]
    context.send.assert_awaited_once_with(embed="test embed")


def test_prefix_rejects_more_than_ten_characters(monkeypatch):
    from src.app.commands.info import prefix as prefix_module

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            raise AssertionError("Invalid prefixes should not query settings")

    monkeypatch.setattr(prefix_module, "GuildSettingsRepository", SettingsRepository)
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    command = Prefix(SimpleNamespace(db=None))

    asyncio.run(Prefix.prefix.callback(command, context, "12345678901"))

    context.send.assert_awaited_once_with(embed="test embed")


def test_prefix_accepts_ten_characters(monkeypatch):
    from src.app.commands.info import prefix as prefix_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(prefix="!")

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(prefix_module, "GuildSettingsRepository", SettingsRepository)
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    command = Prefix(SimpleNamespace(db=None))

    asyncio.run(Prefix.prefix.callback(command, context, "1234567890"))

    assert updates == [(123, {"prefix": "1234567890"})]
    context.send.assert_awaited_once_with(embed="test embed")


def test_language_saves_supported_language(monkeypatch):
    from src.app.commands.settings import language as language_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(language="en-US")

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(
        language_module, "GuildSettingsRepository", SettingsRepository
    )
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    command = Language(SimpleNamespace(db=None))

    asyncio.run(Language.language.callback(command, context, "es"))

    assert updates == [(123, {"language": "es-ES"})]
    context.send.assert_awaited_once_with(embed="test embed")


def test_language_does_not_save_unsupported_language(monkeypatch):
    from src.app.commands.settings import language as language_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(language="en-US")

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(
        language_module, "GuildSettingsRepository", SettingsRepository
    )
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    command = Language(SimpleNamespace(db=None))

    asyncio.run(Language.language.callback(command, context, "fr"))

    assert updates == []
    context.send.assert_awaited_once_with(embed="test embed")


def test_volume_saves_value_and_updates_player(monkeypatch):
    from src.app.commands.music import volume as volume_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(volume=100)

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(
        volume_module, "GuildSettingsRepository", SettingsRepository
    )
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    player = SimpleNamespace(set_volume=AsyncMock())
    context = make_context(player)
    command = Volume(SimpleNamespace(db=None))

    asyncio.run(Volume.volume.callback(command, context, 50))

    assert updates == [(123, {"volume": 50})]
    player.set_volume.assert_awaited_once_with(50)
    context.send.assert_awaited_once_with(embed="test embed")


def test_volume_does_not_save_value_above_one_hundred(monkeypatch):
    from src.app.commands.music import volume as volume_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(volume=100)

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(
        volume_module, "GuildSettingsRepository", SettingsRepository
    )
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    player = SimpleNamespace(set_volume=AsyncMock())
    context = make_context(player)
    command = Volume(SimpleNamespace(db=None))

    asyncio.run(Volume.volume.callback(command, context, 101))

    assert updates == []
    player.set_volume.assert_not_awaited()
    context.send.assert_awaited_once_with(embed="test embed")


def test_autoplay_saves_mode_and_updates_player(monkeypatch):
    from src.app.commands.music import autoplay as autoplay_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(autoplay="disabled")

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(
        autoplay_module, "GuildSettingsRepository", SettingsRepository
    )
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    player = SimpleNamespace(autoplay=None)
    context = make_context(player)
    command = AutoplayCommand(SimpleNamespace(db=None))

    asyncio.run(AutoplayCommand.autoplay.callback(command, context, "partial"))

    assert updates == [(123, {"autoplay": "partial"})]
    assert player.autoplay is wavelink.AutoPlayMode.partial
    context.send.assert_awaited_once_with(embed="test embed")


def test_autoplay_does_not_save_invalid_mode(monkeypatch):
    from src.app.commands.music import autoplay as autoplay_module

    updates = []

    class SettingsRepository:
        def __init__(self, _database):
            pass

        async def read(self, _guild_id):
            return SimpleNamespace(autoplay="disabled")

        async def update(self, guild_id, **values):
            updates.append((guild_id, values))

    monkeypatch.setattr(
        autoplay_module, "GuildSettingsRepository", SettingsRepository
    )
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    command = AutoplayCommand(SimpleNamespace(db=None))

    asyncio.run(AutoplayCommand.autoplay.callback(command, context, "sometimes"))

    assert updates == []
    context.send.assert_awaited_once_with(embed="test embed")
