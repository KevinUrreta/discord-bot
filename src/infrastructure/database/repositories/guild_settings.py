from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.guild_settings import GuildSettingsModel
from src.infrastructure.database.repositories.base import BaseRepository


class GuildSettingsRepository(BaseRepository[GuildSettingsModel]):
    """Repositorio para operaciones CRUD sobre configuraciones de servidor.

    Gestiona la persistencia de preferencias personalizadas por servidor.

    :param database: Instancia de la base de datos.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(GuildSettingsModel, database)
