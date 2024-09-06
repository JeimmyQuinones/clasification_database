from api.application.models.databasec.scan_model import ScanDatabaseModel
from api.application.services.database_services.database_services_interface import (
    DatabaseServiceInterface,
)
from api.application.models.databasec.save_model import SaveDatabaseModel
from typing import Dict
from api.application.use_cases.databasec.save_database_use_case import DatabaseUseCase
from api.application.use_cases.databasec.scan_use_case import ScanUseCase
from api.application.use_cases.databasec.get_data_scan_use_case import (
    GetDataScanUseCase,
)
from api.application.use_cases.databasec.report_use_case import ReportScanUseCase


class DatabaseServiceImpl(DatabaseServiceInterface):

    def __init__(
        self,
        database_use_case: DatabaseUseCase,
        scan_use_case: ScanUseCase,
        get_scan_use_case=GetDataScanUseCase,
        report_scan_use_case=ReportScanUseCase,
    ) -> None:
        self.database_use_case = database_use_case
        self.scan_use_case = scan_use_case
        self.get_scan_use_case = get_scan_use_case
        self.report_scan_use_case = report_scan_use_case

    def Save_database_info(
        self, database_request: SaveDatabaseModel, user_id: int
    ) -> Dict[str, str]:
        data_response = self.database_use_case.save_data_use_case(
            database_request, user_id
        )
        return data_response

    def scan_database_by_id(self, scan_data: ScanDatabaseModel) -> Dict[str, str]:
        data_response = self.scan_use_case.scan_use_case(scan_data)
        return data_response

    def get_scan_database_by_id(self, id: str) -> Dict[str, str]:
        data_response = self.get_scan_use_case.get_data_scan_use_case(id)
        return data_response

    def report_scan_database_by_id(self, id: str) -> Dict[str, str]:
        data_response = self.report_scan_use_case.report_scan_use_case(id)
        return data_response
