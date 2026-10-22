from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.repositories.base import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, database: Database) -> None:
        super().__init__(UserModel, database)