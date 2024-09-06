from collections import defaultdict
from typing import List
from fastapi import HTTPException, status
from api.application.models.databasec.get_scan import (
    GetScanDomain,
    GetScanTable,
    GetScanTableDetail,
)
from api.domain.repositories.database_repository_interface import (
    DatabaseRepositoryInterface,
)
from api.application.config.dependencies.domain_dependencies import get_database_domain


class GetDataScanUseCase:

    dominio_database: DatabaseRepositoryInterface

    def __init__(self) -> None:
        super().__init__()
        self.dominio_database = get_database_domain()

    def get_data_scan_use_case(self, id: str) -> dict:
        """
        Obtiene y organiza los datos de escaneo para una base de datos específica y versión de escaneo.
        """

        self._validate_input(id)
        existing_entry = self.dominio_database.get_databasec_by_id(id)
        self._validate_existing_database(existing_entry)
        data_scan = self.dominio_database.get_scan_data_by_id(
            id, existing_entry.lates_scan_version
        )
        list_result = self._order_data_scan(data_scan)
        return list_result

    def _order_data_scan(self, data_scan):
        """
        Organiza los datos de escaneo en una estructura jerárquica
        basada en dominios, tablas y detalles de columnas.
        """
        list_result: List[GetScanDomain] = []

        grouped_by_domain = defaultdict(list)
        for entity in data_scan:
            grouped_by_domain[entity.domain_name].append(entity)

        for domain_name, grouped_entities in grouped_by_domain.items():
            domain_item = GetScanDomain(nameDatabase=domain_name)
            grouped_by_table = defaultdict(list)
            for entity in grouped_entities:
                grouped_by_table[entity.table_name].append(entity)

            for table_name, grouped_table in grouped_by_table.items():
                table_item = GetScanTable(nameTable=table_name)
                grouped_by_detail = defaultdict(list)
                for entity in grouped_table:
                    grouped_by_detail[entity.detail_column_name].append(entity)
                for detail_column_name, grouped_detail in grouped_by_detail.items():
                    type_identified = (
                        grouped_detail[0].type_description if grouped_detail else None
                    )
                    detail_item = GetScanTableDetail(
                        nameColumn=detail_column_name, typeIdentified=type_identified
                    )
                    table_item.listColum.append(detail_item)
                domain_item.listTable.append(table_item)
            list_result.append(domain_item)
        return list_result

    def _validate_existing_database(self, existing_entry):
        """
        Valida si la base de datos existe y ha sido escaneada.
        """
        if existing_entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La base de datos no existe.",
            )
        if existing_entry.date_scan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La base de no se ha escaneado.",
            )

    def _validate_input(self, id: int):
        """
        Valida la entrada proporcionada.
        """
        if not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos son requeridos",
            )
