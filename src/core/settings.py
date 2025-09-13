from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_PATH = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # bot
    BOT_TOKEN: str | None = None

    # parser
    DNEVNIK_URL: str | None = None
    DNEVNIK_LOGIN: str | None = None
    DNEVNIK_PASS: str | None = None

    # db
    DB_HOST: str | None = None
    DB_PASS: str | None = None
    DB_USER: str | None = None
    DB_NAME: str | None = None
    DB_PORT: int | None = None

    # customization
    GROUP_NAME: str | None = ""
    WEEKS_TOTAL: int | None = 4

    @property
    def DB_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DB_URL_SYNC(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_PATH / ".env")


settings = Settings()
