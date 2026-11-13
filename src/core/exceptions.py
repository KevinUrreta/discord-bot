from discord.ext import commands


class CheckFailure(commands.CheckFailure):
    """Excepción base para fallos en verificaciones de comandos."""


class VoiceChannelRequired(CheckFailure):
    """Excepción lanzada cuando se requiere estar en un canal de voz."""


class SameVoiceChannelRequired(CheckFailure):
    """Excepción lanzada cuando se requiere estar en el mismo canal de voz."""


class ManageMessagesRequired(CheckFailure):
    """Excepción lanzada cuando se requiere permiso de gestionar mensajes."""


class ManageGuildRequired(CheckFailure):
    """Excepción lanzada cuando se requiere permiso de gestionar servidor."""


class NotPlaying(CheckFailure):
    """Excepción lanzada cuando no hay música reproduciéndose."""
