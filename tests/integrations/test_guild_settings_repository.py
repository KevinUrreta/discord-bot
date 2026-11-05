import asyncio

from src.infrastructure.database.connection import Database
from src.infrastructure.database.models import Base
from src.infrastructure.database.repositories.guild import GuildRepository
from src.infrastructure.database.repositories.guild_settings import (
    GuildSettingsRepository,
)


async def _exercise_repository() -> None:
    database = Database("sqlite+aiosqlite:///:memory:")
    try:
        async with database.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        guilds = GuildRepository(database)
        settings = GuildSettingsRepository(database)

        await guilds.create(id=123, name="Test guild")
        created = await settings.update(123, prefix="?")
        assert created is not None
        assert created.prefix == "?"

        loaded = await settings.read(123)
        assert loaded is not None
        assert loaded.prefix == "?"
        assert loaded.language == "en"
        assert loaded.volume == 100
        assert loaded.autoplay == "disabled"

        updated = await settings.update(123, language="es", volume=75)
        assert updated is not None
        assert updated.language == "es"
        assert updated.volume == 75

        assert await settings.delete(123) is True
        assert await settings.read(123) is None
    finally:
        await database.close()


def test_guild_settings_repository_against_in_memory_database() -> None:
    asyncio.run(_exercise_repository())
