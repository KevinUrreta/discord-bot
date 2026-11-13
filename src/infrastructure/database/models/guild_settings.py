from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.connection import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models.guild import GuildModel


class GuildSettingsModel(Base):
    """Modelo ORM para la tabla de configuraciones por servidor.

    Almacena preferencias personalizadas de cada servidor como prefijo,
    idioma, volumen y modo de reproducción automática.
    """

    __tablename__ = "guild_settings"

    guild_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guilds.id", ondelete="CASCADE"), primary_key=True
    )

    prefix: Mapped[str] = mapped_column(String(10), default="!", nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    volume: Mapped[int] = mapped_column(default=100, nullable=False)
    autoplay: Mapped[str] = mapped_column(
        String(20), default="disabled", nullable=False
    )

    guild: Mapped["GuildModel"] = relationship(back_populates="settings")
