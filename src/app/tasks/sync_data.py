
import logging
from datetime import datetime

from discord.ext import commands, tasks

from src.app.client import Client
from src.infrastructure.database.repositories.guild import GuildRepository
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository
from src.infrastructure.database.repositories.member import MemberRepository
from src.infrastructure.database.repositories.user import UserRepository

logger = logging.getLogger("discord")


class SyncData(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.sync_db_loop.start()

    def cog_unload(self):
        self.sync_db_loop.cancel()

    @tasks.loop(minutes=30)
    async def sync_db_loop(self) -> None:
        try:
            guilds = GuildRepository(self.client.db)
            settings = GuildSettingsRepository(self.client.db)
            users = UserRepository(self.client.db)
            members = MemberRepository(self.client.db)

            active_guild_ids = {guild.id for guild in self.client.guilds}
            active_members: set[tuple[int, int]] = set()

            for guild in self.client.guilds:
                db_guild = await guilds.read(guild.id)
                if db_guild is None:
                    await guilds.create(id=guild.id, name=guild.name)
                    if await settings.read(guild.id) is None:
                        await settings.create(guild_id=guild.id)
                elif db_guild.name != guild.name:
                    await guilds.update(guild.id, name=guild.name)

                async for member in guild.fetch_members(limit=None):
                    active_members.add((guild.id, member.id))

                    user = await users.read(member.id)
                    if user is None:
                        await users.create(id=member.id, username=member.name)
                    elif user.username != member.name:
                        await users.update(member.id, username=member.name)

                    data: dict[str, str | datetime | None] = {
                        "nickname": member.nick
                    }

                    if member.joined_at is not None:
                        data["joined_guild_at"] = member.joined_at

                    db_member = await members.read(guild.id, member.id)
                    if db_member is None:
                        await members.create(
                            guild_id=guild.id,
                            user_id=member.id,
                            **data,
                        )
                    elif any(
                        getattr(db_member, key) != value
                        for key, value in data.items()
                    ):
                        await members.update(guild.id, member.id, **data)

            for member in await members.list_all():
                key = (member.guild_id, member.user_id)
                if member.guild_id in active_guild_ids and key not in active_members:
                    await members.delete(*key)

            for guild in await guilds.list_all():
                if guild.id not in active_guild_ids:
                    await guilds.delete(guild.id)

            logger.info("Sincronización completa finalizada.")

        except Exception as e:
            logger.exception(f"Error durante la sincronización de la base de datos: {e}")

    @sync_db_loop.before_loop
    async def before_sync_db_loop(self) -> None:
        await self.client.wait_until_ready()
