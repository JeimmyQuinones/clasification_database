from datetime import datetime
from sqlalchemy import CHAR, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from api.infrastructure.database.connector import Base


class ScanDomainDBModel(Base):
    __tablename__ = "scanDomain"

    id = Column(CHAR(36), primary_key=True, unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    database_id = Column(CHAR(36), ForeignKey("databaseScan.id"), nullable=False)
    version_scan = Column(Integer, nullable=False)
    date_scan = Column(DateTime, default=datetime.now, nullable=False)

    database = relationship("DatabaseDBModel", back_populates="scan_domain")
    scan_tables = relationship("ScanTablesDBModel", back_populates="scan_domain")
