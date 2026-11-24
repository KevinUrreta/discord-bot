from datetime import datetime

from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed
from src.infrastructure.database.repositories.guild import GuildRepository
from src.infrastructure.database.repositories.guild_settings import (
    GuildSettingsRepository,
)
from src.infrastructure.database.repositories.member import MemberRepository
from src.infrastructure.database.repositories.user import UserRepository


class Server(commands.Cog):
    """Componente que muestra estadísticas del servidor."""

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx: commands.Context) -> None:
        """Muestra estadísticas del servidor."""

        guild = ctx.guild
        if guild is None:
            return

        guild_repo = GuildRepository(self.client.db)
        settings_repo = GuildSettingsRepository(self.client.db)
        members_repo = MemberRepository(self.client.db)
        users_repo = UserRepository(self.client.db)

        db_guild = await guild_repo.read(guild.id)
        db_settings = await settings_repo.read(guild.id)

        all_members = await members_repo.list_all()
        guild_members = [m for m in all_members if m.guild_id == guild.id]

        member_count_db = len(guild_members)

        unique_user_ids = {m.user_id for m in guild_members}
        user_count_db = len(unique_user_ids)

        if guild_members:
            try:
                oldest_member = min(
                    guild_members,
                    key=lambda m: m.joined_guild_at or datetime.min,
                )
                oldest_user = await users_repo.read(oldest_member.user_id)
                oldest_name = oldest_user.username if oldest_user else "Desconocido"
            except Exception:
                oldest_name = "No disponible"
        else:
            oldest_name = "No disponible"

        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.info.guild.stats",
                guild_name=guild.name,
                guild_id=guild.id,
                db_guild_name=db_guild.name if db_guild else None,
                member_count=member_count_db,
                user_count=user_count_db,
                prefix=db_settings.prefix if db_settings else "!",
                language=db_settings.language if db_settings else "en",
                volume=db_settings.volume if db_settings else 100,
                autoplay=db_settings.autoplay if db_settings else "disabled",
                oldest_name=oldest_name,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )
