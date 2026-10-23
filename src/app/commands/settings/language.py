from discord.ext import commands

from src.helpers.embed import CustomEmbed
from src.i18n.translate import translator
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


class Language(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="language", aliases=["lang"])
    async def language(self, ctx: commands.Context, language: str | None = None) -> None:
        guild = ctx.guild
        if guild is None:
            return

        repo = GuildSettingsRepository(self.client.db)
        settings = await repo.read(guild.id)
        current = settings.language

        if language is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.settings.language.current_language",
                language=current,
                supported=translator.get_supported_languages(),
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        normalized = translator.normalize(language)

        if normalized is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.settings.language.not_supported",
                err=language,
                supported=translator.get_supported_languages(),
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        await repo.update(guild.id, language=normalized)
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.settings.language.set_language",
            language=normalized,
            footer_icon=ctx.author.display_avatar.url
        ))
