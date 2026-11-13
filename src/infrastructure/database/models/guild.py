from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.connection import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models.guild_settings import GuildSettingsModel
    from src.infrastructure.database.models.member import MemberModel


class GuildModel(Base):
    """Modelo ORM para la tabla de servidores de Discord.

    Representa la información básica de cada servidor conectado al bot.
    """

    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    settings: Mapped[Optional["GuildSettingsModel"]] = relationship(
        back_populates="guild", cascade="all, delete-orphan", uselist=False
    )

    members: Mapped[list["MemberModel"]] = relationship(
        back_populates="guild", cascade="all, delete-orphan"
    )
