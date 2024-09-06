from collections import defaultdict
from typing import List
from fastapi import HTTPException, status
from api.application.models.databasec.report_scan_model import (
    ClassifiedScanModel,
    HistoricalScanModel,
    LastScanDetail,
    LastScantableDetail,
    ReportScanModel,
)
from api.domain.repositories.database_repository_interface import (
    DatabaseRepositoryInterface,
)
from api.application.config.dependencies.domain_dependencies import get_database_domain


class ReportScanUseCase:

    dominio_database: DatabaseRepositoryInterface

    def __init__(self) -> None:
        super().__init__()
        self.dominio_database = get_database_domain()

    def report_scan_use_case(self, id: str) -> dict:
        """
        Genera un informe de escaneo para una base de datos específica identificada por el `id`.
        """
        self._validate_input(id)
        existing_entry = self.dominio_database.get_databasec_by_id(id)
        self._validate_existing_database(existing_entry)
        data_scan = self.dominio_database.get_report_totals_info_version(id)
        data_scan_type = self.dominio_database.get_report_types_info(id)
        data_scan_last_version_detail = (
            self.dominio_database.get_report_by_version_detail(
                id, existing_entry.lates_scan_version
            )
        )
        response_report = ReportScanModel(
            historical_scan=self._order_historical_info(data_scan, data_scan_type),
            last_scan_detail=self._order_last_detail(data_scan_last_version_detail),
        )
        return response_report

    def _validate_existing_database(self, existing_entry):
        """
        Verifica si la base de datos existe y si ha sido escaneada.
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
        Verifica que el identificador proporcionado sea válido.
        """
        if not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos son requeridos",
            )

    def _order_last_detail(self, data_scan_last_version_detail):
        """
        Ordena y organiza los detalles del escaneo de la última versión por esquema y tabla.

        """
        retult_order_list: List[LastScanDetail] = []
        grouped_by_domain = defaultdict(list)
        for entity in data_scan_last_version_detail:
            grouped_by_domain[entity.domain_name].append(entity)

        for domain_name, grouped_entities in grouped_by_domain.items():
            retult_order = LastScanDetail(name_scheme=domain_name)
            grouped_by_table = defaultdict(list)
            for entity in grouped_entities:
                grouped_by_table[entity.table_name].append(entity)

            for table_name, grouped_table in grouped_by_table.items():
                total_columns = sum(entity.columns for entity in grouped_table)
                total_classified = sum(
                    entity.total_clasification for entity in grouped_table
                )
                percentage_classified = (
                    (total_classified / total_columns) * 100 if total_columns > 0 else 0
                )

                list_tables = LastScantableDetail(
                    name_table=table_name,
                    total_columns=total_columns,
                    total_classified_columns=total_classified,
                    porcentage_classified_columns=percentage_classified,
                )
                retult_order.list_tables_detail.append(list_tables)
            retult_order_list.append(retult_order)
        return retult_order_list

    def _order_historical_info(self, data_scan, data_scan_type):
        """
        Organiza los datos históricos de escaneo, calculando el porcentaje de difeentes datos

        """
        list_historical: List[HistoricalScanModel] = []
        for version in data_scan:
            version_item = HistoricalScanModel(
                version_scan=version.version_scan,
                date_scan=version.date_scan,
                total_schemes_scan=version.total_schemes,
                total_tables_scan=version.total_tablas,
                total_columns_scan=version.total_columnas,
                total_columns_classified_scan=version.total_clasificadas,
                percentage_classified_scan=(
                    version.total_clasificadas / version.total_columnas
                )
                * 100,
                classified_by_type_list_scan=self._order_type_scan_info_by_version(
                    data_scan_type, version.version_scan, version.total_columnas
                ),
            )
            list_historical.append(version_item)
        return list_historical

    def _order_type_scan_info_by_version(self, data_scan_type, version, total_colums):
        """
        Filtra y organiza la información de clasificación por tipo para una versión específica.

        """
        list_result_clasification: List[ClassifiedScanModel] = []
        list_filter = filter(lambda m: m.version_scan == version, data_scan_type)
        for type in list_filter:
            item_type = ClassifiedScanModel(
                type_name=type.name_tipo,
                total_columns=type.total_columnas,
                percentage=(type.total_columnas / total_colums) * 100,
            )
            list_result_clasification.append(item_type)
        return list_result_clasification
