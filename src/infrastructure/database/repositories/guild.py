from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.guild import GuildModel
from src.infrastructure.database.models.guild_settings import GuildSettingsModel
from src.infrastructure.database.repositories.base import BaseRepository

class GuildRepository(BaseRepository[GuildModel]):
    def __init__(self, database: Database) -> None:
        super().__init__(GuildModel, database)

    async def create_or_update(self, guild_id: int, name: str) -> GuildModel:
        async with self.database.get_session() as session:
            stmt = select(GuildModel).options(selectinload(GuildModel.settings)).where(GuildModel.id == guild_id)
            result = await session.execute(stmt)
            guild = result.scalar_one_or_none()

            if guild is not None:
                if guild.name != name:
                    guild.name = name
                    await session.refresh(guild)
                return guild

            guild = GuildModel(id=guild_id, name=name)
            guild.settings = GuildSettingsModel(guild_id=guild_id)
            session.add(guild)
            await session.flush()
            await session.refresh(guild)
            return guild

    async def get(self, guild_id: int) -> GuildModel | None:
        async with self.database.get_session() as session:
            stmt = select(GuildModel).options(selectinload(GuildModel.settings)).where(GuildModel.id == guild_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def delete(self, guild_id: int) -> bool:
        return await self.delete_by_id(guild_id)