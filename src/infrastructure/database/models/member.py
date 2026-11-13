from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.connection import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models.guild import GuildModel
    from src.infrastructure.database.models.user import UserModel


class MemberModel(Base):
    """Modelo ORM para la tabla de miembros en servidores.

    Representa la relación entre usuarios y servidores con información
    adicional como apodo y fecha de unión al servidor.
    """

    __tablename__ = "members"

    guild_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guilds.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    nickname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    joined_guild_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    guild: Mapped["GuildModel"] = relationship(back_populates="members")
    user: Mapped["UserModel"] = relationship(back_populates="memberships")
