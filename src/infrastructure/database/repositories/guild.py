from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.guild import GuildModel
from src.infrastructure.database.repositories.base import BaseRepository


class GuildRepository(BaseRepository[GuildModel]):
    """Repositorio para operaciones CRUD sobre servidores.

    Gestiona la persistencia de información de servidores en la base de datos.

    :param database: Instancia de la base de datos.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(GuildModel, database)
