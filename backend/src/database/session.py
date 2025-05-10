
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.crawler.config import settings
from src.database.base import Base # type: ignore

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

init_db()