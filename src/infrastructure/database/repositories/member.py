from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.member import MemberModel
from src.infrastructure.database.repositories.base import BaseRepository


class MemberRepository(BaseRepository[MemberModel]):
    """Repositorio para operaciones CRUD sobre miembros de servidores.

    Gestiona la persistencia de relaciones usuario-servidor.

    :param database: Instancia de la base de datos.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(MemberModel, database)
