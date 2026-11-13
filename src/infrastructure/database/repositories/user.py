from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """Repositorio para operaciones CRUD sobre usuarios.

    Gestiona la persistencia de información de usuarios en la base de datos.

    :param database: Instancia de la base de datos.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(UserModel, database)
