import os

from pydantic import PostgresDsn, computed_field 
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class XingSettings(BaseSettings):
    XING_APP_KEY: str
    XING_APP_SECRET: str
    SQLITE_DB_FILE: str = "./tg_crawler.db"
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"sqlite:///../{self.SQLITE_DB_FILE}"

    class Config:
        env_file = (
            ".env.dev.xing" if os.getenv("ENVIRONMENT", "DEV") == 'DEV' else
            ".env.stage.xing" if os.getenv("ENVIRONMENT", "STAGE") == 'STAGE' else
            ".env.prod.xing" if os.getenv("ENVIRONMENT", "PROD") == 'PROD' else
            ".env.xing"
        )
        env_file_encoding = "utf-8"

settings = XingSettings() # type: ignore