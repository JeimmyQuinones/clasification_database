from sqlalchemy import CHAR, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.infrastructure.database.connector import Base


class ScanDetailTablesDBModel(Base):
    __tablename__ = "scanDetailTables"

    id = Column(CHAR(36), primary_key=True, unique=True, nullable=False)
    table_id = Column(CHAR(36), ForeignKey("scanTables.id"), nullable=False)
    nameColumn = Column(String(200), nullable=False)
    typeIdentified_id = Column(
        Integer, ForeignKey("typeIdentifiedData.id"), nullable=False
    )

    typeIdentified_data = relationship(
        "TypeIdentifiedDataDBModel", back_populates="scan_detailtable"
    )
    scan_table = relationship("ScanTablesDBModel", back_populates="scan_detailtables")
