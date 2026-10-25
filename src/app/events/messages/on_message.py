import logging

import discord
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        channel_name = getattr(message.channel, "name", "DM")

        if message.embeds:
            embed_messages = []

            for embed in message.embeds:
                embed_info = []

                if embed.title:
                    embed_info.append(f"Title: {embed.title}")
                if embed.description:
                    embed_info.append(f"Description: {embed.description}")
                if embed.url:
                    embed_info.append(f"URL: {embed.url}")
                if embed.type:
                    embed_info.append(f"Type: {embed.type}")

                if embed.author and embed.author.name:
                    author_info = embed.author.name
                    if embed.author.url:
                        author_info += f" ({embed.author.url})"
                    embed_info.append(f"Author: {author_info}")

                for field in embed.fields:
                    embed_info.append(f"Field: {field.name} = {field.value}")

                if embed.footer and embed.footer.text:
                    footer_info = embed.footer.text
                    if embed.footer.icon_url:
                        footer_info += f" ({embed.footer.icon_url})"
                    embed_info.append(f"Footer: {footer_info}")

                if embed.thumbnail and embed.thumbnail.url:
                    embed_info.append(f"Thumbnail: {embed.thumbnail.url}")
                if embed.image and embed.image.url:
                    embed_info.append(f"Image: {embed.image.url}")
                if embed.timestamp:
                    embed_info.append(f"Timestamp: {embed.timestamp}")

                embed_messages.append(" | ".join(embed_info))

            message_content = " || ".join(embed_messages)

        else:
            message_content = message.content

        logger.info(
            f"Server: {message.guild.name} | Channel: #{channel_name} | "
            f"Author: {message.author.name} | Message: {message_content}"
        )
