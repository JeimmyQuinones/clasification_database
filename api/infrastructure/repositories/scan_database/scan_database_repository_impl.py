from typing import List
from fastapi import HTTPException, status
from sqlalchemy import MetaData, inspect
from sqlalchemy.orm import Session
from api.domain.entities.scan_table_info import (
    GetDomainInfoEntity,
    GetTableInfoEntity,
)
from api.domain.repositories.scan_database_repository_interface import (
    ScanDatabaseRepositoryInterface,
)
from api.infrastructure.database.connector import get_db_connection_by_Url
from sqlalchemy.exc import SQLAlchemyError


class ScanDatabaseRepositoryImpl(ScanDatabaseRepositoryInterface):

    def get_info_by_database(self, url: str) -> None:
        try:
            session: Session = next(get_db_connection_by_Url(url))
            print("Session Bind:", session.bind)
            inspector = inspect(session.bind)
            database = inspector.get_schema_names()
            session.remove()
            return database
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error al conectar a la base de datos: {e}",
            )

    def get_database_info(self, url: str, database: str) -> None:
        try:
            db_url = f"{url}/{database}"
            session2: Session = next(get_db_connection_by_Url(db_url))
            metadata = MetaData()
            metadata.reflect(bind=session2.bind)
            tables_info: List[GetTableInfoEntity] = []
            for table_name, table in metadata.tables.items():
                scan_item = GetTableInfoEntity(
                    name_table=table_name,
                    colum_list=[column.name for column in table.columns],
                )
                tables_info.append(scan_item)
            database_info = GetDomainInfoEntity(
                nameDatabase=database, table_list=tables_info
            )
            session2.close()
            return database_info
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error al conectar a la base de datos: {e}",
            )
