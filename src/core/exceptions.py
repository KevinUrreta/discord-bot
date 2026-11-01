from discord.ext import commands

class CheckFailure(commands.CheckFailure):
    pass

class VoiceChannelRequired(CheckFailure):
    pass

class SameVoiceChannelRequired(CheckFailure):
    pass

class ManageMessagesRequired(CheckFailure):
    pass

class ManageGuildRequired(CheckFailure):
    pass

class NotPlaying(CheckFailure):
    pass
