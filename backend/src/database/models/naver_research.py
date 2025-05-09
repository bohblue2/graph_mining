
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        LargeBinary, String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.base import Base


class NaverResearchReportOrm(Base):
    __tablename__ = 'naver_research_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    file_url = Column(String, nullable=False)
    issuer_company_name = Column(String, nullable=False)
    issuer_company_id = Column(String, nullable=False)
    report_category = Column(String, nullable=False)
    target_company  = Column(String, nullable=True)
    target_industry = Column(String, nullable=True)
    downloaded = Column(Boolean, nullable=True)
    files = relationship('NaverResearchReportFileOrm', backref='naver_research_report', cascade='all, delete-orphan')
    chunks = relationship('NaverResearchReportChunkOrm', backref='naver_research_report', cascade='all, delete-orphan')
    chunked_at = Column(DateTime(timezone=True), nullable=True, default=None)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        attributes = (
            f"id={self.id}",
            f"report_id='{self.report_id}'",
            f"title='{self.title}'",
            f"date='{self.date}'",
            f"file_url='{self.file_url}'",
            f"issuer_company_name='{self.issuer_company_name}'",
            f"issuer_company_id='{self.issuer_company_id}'",
            f"report_category='{self.report_category}'",
            f"target_company='{self.target_company}'",
            f"target_industry='{self.target_industry}'",
            f"downloaded={self.downloaded}",
            f"updated_at='{self.updated_at}'",
            f"created_at='{self.created_at}'"
        )
        return f"<NaverResearchReportOrm({', '.join(attributes)})>"

class NaverResearchReportFileOrm(Base):
    __tablename__ = 'naver_research_report_files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey('naver_research_reports.id'), nullable=False)
    file_data = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return f"<NaverResearchReportFileOrm(id={self.id}, report_id={self.report_id}, created_at='{self.created_at}')>"

class NaverResearchReportChunkOrm(Base):
    __tablename__ = 'naver_research_report_chunks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey('naver_research_reports.id'), nullable=False)
    chunk_num = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    embedded_at = Column(DateTime(timezone=True), nullable=True, default=None)
    tags = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        attributes = (
            f"id={self.id}",
            f"report_id={self.report_id}",
            f"chunk_num={self.chunk_num}",
            f"content='{self.content}'",
            f"embedded_at='{self.embedded_at}'",
            f"tags='{self.tags}'",
            f"created_at='{self.created_at}'"
        )
        return f"<NaverResearchReportChunkOrm({', '.join(attributes)})>"