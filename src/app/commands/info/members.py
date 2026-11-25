from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed
from src.infrastructure.database.repositories.member import MemberRepository
from src.infrastructure.database.repositories.user import UserRepository


class Members(commands.Cog):
    """Componente que muestra información de los miembros del servidor."""

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="membersinfo")
    async def members_info(self, ctx: commands.Context) -> None:
        """Muestra estadísticas de miembros del servidor.

        :param ctx: Contexto del comando de Discord.
        """

        guild = ctx.guild
        if guild is None:
            return

        members_repo = MemberRepository(self.client.db)
        users_repo = UserRepository(self.client.db)

        all_members = await members_repo.list_all()
        guild_members = [m for m in all_members if m.guild_id == guild.id]

        user_ids = list({m.user_id for m in guild_members})
        user_names = []

        for uid in user_ids:
            user = await users_repo.read(uid)

            if user:
                member = guild.get_member(uid)
                nickname = member.display_name if member else user.username

                user_names.append(f"{user.username} ({nickname})")

        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.info.members.stats",
                member_count=len(guild_members),
                user_names="\n".join(user_names) if user_names else None,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )
