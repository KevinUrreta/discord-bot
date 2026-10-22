from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.guild import GuildModel
from src.infrastructure.database.repositories.base import BaseRepository

class GuildRepository(BaseRepository[GuildModel]):
    def __init__(self, database: Database) -> None:
        super().__init__(GuildModel, database)