from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    lavalink_password: str
    lavalink_port: str
    lavalink_opus: str

    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str = "postgres"
    postgres_port: str = "5432"

    @property
    def postgres_url(self) -> str:
        return str(
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password.get_secret_value()}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )