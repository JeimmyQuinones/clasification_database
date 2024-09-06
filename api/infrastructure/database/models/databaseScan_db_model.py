from datetime import datetime
from sqlalchemy import CHAR, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.infrastructure.database.connector import Base


class DatabaseDBModel(Base):
    __tablename__ = "databaseScan"

    id = Column(CHAR(36), primary_key=True, unique=True, nullable=False)
    host = Column(String(50), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    date_create = Column(DateTime, default=datetime.now, nullable=False)
    date_scan = Column(DateTime, nullable=True)
    lates_version = Column(Integer, nullable=True)

    user_create_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    scan_domain = relationship("ScanDomainDBModel", back_populates="database")
    user = relationship("UserDBModel", back_populates="database_tables")
