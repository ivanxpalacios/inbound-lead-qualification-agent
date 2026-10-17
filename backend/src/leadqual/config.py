from typing import Literal
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]  # leadqual → src → backend

class Settings(BaseSettings):
    app_name: str = "Inbound Lead Qualification Agent API"
    environment: Literal["development", "test", "production"] = "development"
    debug: bool = False
    database_url: SecretStr

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()