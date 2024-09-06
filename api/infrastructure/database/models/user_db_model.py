from sqlalchemy import Column, DateTime, String, Integer
from api.infrastructure.database.connector import Base
from datetime import datetime

from sqlalchemy.orm import relationship


class UserDBModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    date_create = Column(DateTime, default=datetime.now, nullable=False)

    database_tables = relationship("DatabaseDBModel", back_populates="user")
