from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.guild_settings import GuildSettingsModel
from src.infrastructure.database.repositories.base import BaseRepository

class GuildSettingsRepository(BaseRepository[GuildSettingsModel]):
    def __init__(self, database: Database) -> None:
        super().__init__(GuildSettingsModel, database)