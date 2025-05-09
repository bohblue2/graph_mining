import os

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class CrawlerSettings(BaseSettings):
    # 선택할 데이터베이스 엔진: "postgres" | "sqlite"
    DB_ENGINE: str = "sqlite"

    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_SERVER: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_DB: str | None = None

    SQLITE_DB_FILE: str = "./tg_crawler.db"

    ALEMBIC_DB_URL: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        if self.DB_ENGINE.lower() == "postgres":
            url = MultiHostUrl.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
            return str(url)
        return f"sqlite:///../{self.SQLITE_DB_FILE}"
    
    def __post_init__(self):
        def display_all_fields(self):
            """
            Display all configuration values.
            """
            for field_name, field_value in self.__dict__.items():
                print(f"{field_name}: {field_value}")
        display_all_fields(self)
    
    class Config:
        env_file = (
            ".env.dev.crawler" if os.getenv("ENVIRONMENT", "DEV") == 'DEV' else
            ".env.stage.crawler" if os.getenv("ENVIRONMENT", "STAGE") == 'STAGE' else
            ".env.prod.crawler" if os.getenv("ENVIRONMENT", "PROD") == 'PROD' else
            ".env.crawler"
        )
        env_file_encoding = "utf-8"

settings = CrawlerSettings() # type: ignore