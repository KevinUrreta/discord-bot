from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )
    discord_token: SecretStr

    log_file: str = "./logs/discord.log"

    lavalink_host: str
    lavalink_password: SecretStr
    lavalink_port: str
    lavalink_opus: str

    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str = "postgres"
    postgres_port: str = "5432"

    @property
    def postgres_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=int(self.postgres_port),
            database=self.postgres_db,
        )
