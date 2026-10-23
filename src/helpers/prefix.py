import discord

from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


async def get_prefix(client, message: discord.Message) -> str:
    if not message.guild:
        return "!"
    repo = GuildSettingsRepository(client.db)
    settings = await repo.read(message.guild.id)
    if settings is None:
        return "!"
    if settings.prefix == "<" and message.content.startswith("<@"):
        return "\0"
    if settings and settings.prefix:
        return settings.prefix
    else:
        return "!"
