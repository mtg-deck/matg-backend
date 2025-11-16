from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    API_KEY: str
    CLIENT_ID: str
    DATABASE_URL: str
    API_URL: str
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding="utf-8")


settings = Settings()
