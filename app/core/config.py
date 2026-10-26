"""Read and validate application configuration."""

from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """System environment variables override values in the project .env file."""

    model_config = SettingsConfigDict(
        env_prefix="KH_",
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "KnowledgeHub"
    debug: bool = False
    database_url: SecretStr


settings = Settings()
