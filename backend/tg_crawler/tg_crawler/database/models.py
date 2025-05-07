from sqlalchemy import Column, DateTime, Integer, String, func
from tg_crawler.database.base import Base


class NaverThemeListOrm(Base):
    __tablename__ = 'naver_theme_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)


class NaverThemeDetailOrm(Base):
    __tablename__ = 'naver_theme_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_name = Column(String, nullable=False)
    stock_name = Column(String, nullable=False)
    discussion_url = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)