from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.connection import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models.member import MemberModel


class UserModel(Base):
    """Modelo ORM para la tabla de usuarios de Discord.

    Representa la información básica de cada usuario que interactúa con el bot.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    memberships: Mapped[list["MemberModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
