from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch
import uuid

from fastapi import HTTPException
from api.application.models.databasec.report_scan_model import (
    ClassifiedScanModel,
    HistoricalScanModel,
    LastScanDetail,
    LastScantableDetail,
    ReportScanModel,
)
from api.application.use_cases.databasec.report_use_case import ReportScanUseCase
from api.domain.entities.databaseC import DatabaseEntity
from api.domain.entities.report_total_version import (
    ReportDetailVersionEntity,
    ReportTotalVersionEntity,
    ReportTypeVersionEntity,
)


class TestReportUseCase(unittest.TestCase):

    @patch("api.application.use_cases.databasec.report_use_case.get_database_domain")
    def test_report_scan_use_case_entry_not_found(self, mock_get_database_domain):
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_id.return_value = None
        mock_repo.get_report_totals_info_version.return_value = None
        mock_repo.get_report_types_info.return_value = None
        mock_repo.get_report_by_version_detail.return_value = None
        mock_get_database_domain.return_value = mock_repo

        data_id = "_id_id"
        use_case = ReportScanUseCase()

        with self.assertRaises(HTTPException) as context:
            use_case.report_scan_use_case(data_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 404)

    @patch("api.application.use_cases.databasec.report_use_case.get_database_domain")
    def test_report_scan_use_case_no_scan_date(self, mock_get_database_domain):
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_id.return_value = DatabaseEntity(
            id=uuid.uuid4(),
            host="db_data.host",
            port=1234,
            username="db_data.username",
            password="db_data.password",
            user_id=1,
        )
        mock_repo.get_report_totals_info_version.return_value = None
        mock_repo.get_report_types_info.return_value = None
        mock_repo.get_report_by_version_detail.return_value = None
        mock_get_database_domain.return_value = mock_repo

        data_id = "_id_id"
        use_case = ReportScanUseCase()

        with self.assertRaises(HTTPException) as context:
            use_case.report_scan_use_case(data_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 404)

    @patch("api.application.use_cases.databasec.report_use_case.get_database_domain")
    def test_report_scan_use_case_input_invalid(self, mock_get_database_domain):
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_id.return_value = None
        mock_repo.get_report_totals_info_version.return_value = None
        mock_repo.get_report_types_info.return_value = None
        mock_repo.get_report_by_version_detail.return_value = None
        mock_get_database_domain.return_value = mock_repo

        data_id = ""
        use_case = ReportScanUseCase()

        with self.assertRaises(HTTPException) as context:
            use_case.report_scan_use_case(data_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 400)

    @patch("api.application.use_cases.databasec.report_use_case.get_database_domain")
    def test_report_scan_use_case_successful_report(self, mock_get_database_domain):
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_id.return_value = DatabaseEntity(
            id=uuid.uuid4(),
            host="db_data.host",
            port=1234,
            username="db_data.username",
            password="db_data.password",
            user_id=1,
            date_scan=datetime(2024, 7, 4, 19, 0),
            lates_scan_version=1,
        )
        mock_repo.get_report_totals_info_version.return_value = [
            ReportTotalVersionEntity(
                total_tablas=2,
                total_columnas=2,
                total_clasificadas=2,
                version_scan=1,
                date_scan=datetime(2024, 7, 4, 19, 0),
                total_schemes=1,
            ),
            ReportTotalVersionEntity(
                total_tablas=2,
                total_columnas=2,
                total_clasificadas=2,
                version_scan=1,
                date_scan=datetime(2024, 7, 4, 19, 0),
                total_schemes=1,
            ),
        ]
        mock_repo.get_report_types_info.return_value = [
            ReportTypeVersionEntity(
                name_tipo="name_tipo",
                total_columnas=2,
                version_scan=1,
            ),
            ReportTypeVersionEntity(
                name_tipo="name_tipo",
                total_columnas=2,
                version_scan=1,
            ),
        ]
        mock_repo.get_report_by_version_detail.return_value = [
            ReportDetailVersionEntity(
                domain_name="domain_name",
                domain_id="domain_id",
                table_name="table_name",
                columns=2,
                total_clasification=2,
            ),
            ReportDetailVersionEntity(
                domain_name="domain_name",
                domain_id="domain_id",
                table_name="table_name",
                columns=2,
                total_clasification=2,
            ),
        ]
        mock_get_database_domain.return_value = mock_repo

        data_id = "id_di"
        use_case = ReportScanUseCase()

        result = use_case.report_scan_use_case(data_id)
        result_expected = ReportScanModel(
            historical_scan=[
                HistoricalScanModel(
                    version_scan=1,
                    date_scan=datetime(2024, 7, 4, 19, 0),
                    total_schemes_scan=1,
                    total_tables_scan=2,
                    total_columns_scan=2,
                    total_columns_classified_scan=2,
                    percentage_classified_scan=100.0,
                    classified_by_type_list_scan=[
                        ClassifiedScanModel(
                            type_name="name_tipo", total_columns=2, percentage=100.0
                        ),
                        ClassifiedScanModel(
                            type_name="name_tipo", total_columns=2, percentage=100.0
                        ),
                    ],
                ),
                HistoricalScanModel(
                    version_scan=1,
                    date_scan=datetime(2024, 7, 4, 19, 0),
                    total_schemes_scan=1,
                    total_tables_scan=2,
                    total_columns_scan=2,
                    total_columns_classified_scan=2,
                    percentage_classified_scan=100.0,
                    classified_by_type_list_scan=[
                        ClassifiedScanModel(
                            type_name="name_tipo", total_columns=2, percentage=100.0
                        ),
                        ClassifiedScanModel(
                            type_name="name_tipo", total_columns=2, percentage=100.0
                        ),
                    ],
                ),
            ],
            last_scan_detail=[
                LastScanDetail(
                    name_scheme="domain_name",
                    list_tables_detail=[
                        LastScantableDetail(
                            name_table="table_name",
                            total_columns=4,
                            total_classified_columns=4,
                            porcentage_classified_columns=100.0,
                        )
                    ],
                )
            ],
        )

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(result, result_expected)
