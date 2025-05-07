
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tg_crawler.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from tg_crawler.database.models import Base # type: ignore
    Base.metadata.create_all(bind=engine)

init_db()