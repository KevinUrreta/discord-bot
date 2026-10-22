from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.member import MemberModel
from src.infrastructure.database.repositories.base import BaseRepository

class MemberRepository(BaseRepository[MemberModel]):
    def __init__(self, database: Database) -> None:
        super().__init__(MemberModel, database)