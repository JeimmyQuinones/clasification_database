from sqlalchemy import CHAR, Column, String, ForeignKey
from sqlalchemy.orm import relationship


from api.infrastructure.database.connector import Base


class ScanTablesDBModel(Base):
    __tablename__ = "scanTables"

    id = Column(CHAR(36), primary_key=True, unique=True, nullable=False)
    domain_id = Column(CHAR(36), ForeignKey("scanDomain.id"), nullable=False)
    name = Column(String(200), nullable=False)

    scan_domain = relationship("ScanDomainDBModel", back_populates="scan_tables")
    scan_detailtables = relationship(
        "ScanDetailTablesDBModel", back_populates="scan_table"
    )
