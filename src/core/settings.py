from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.config import BASE_PATH


class Settings(BaseSettings):
    # bot
    BOT_TOKEN: str

    # parser
    DNEVNIK_URL: str
    DNEVNIK_LOGIN: str
    DNEVNIK_PASS: str

    # db
    DB_HOST: str
    DB_PASS: str
    DB_USER: str
    DB_NAME: str
    DB_PORT: int

    @property
    def DB_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_PATH / ".env")


settings = Settings()
