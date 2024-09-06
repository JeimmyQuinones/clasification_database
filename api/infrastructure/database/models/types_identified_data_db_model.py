from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from api.infrastructure.database.connector import Base


class TypeIdentifiedDataDBModel(Base):
    __tablename__ = "typeIdentifiedData"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    alias = Column(String(100), nullable=False)

    scan_detailtable = relationship(
        "ScanDetailTablesDBModel", back_populates="typeIdentified_data"
    )
