from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch
import uuid

from fastapi import HTTPException
from api.application.models.databasec.get_scan import (
    GetScanDomain,
    GetScanTable,
    GetScanTableDetail,
)
from api.application.use_cases.databasec.get_data_scan_use_case import (
    GetDataScanUseCase,
)
from api.domain.entities.databaseC import DatabaseEntity, ScanDatabaseById


class TestGetScanUseCase(unittest.TestCase):

    @patch(
        "api.application.use_cases.databasec.get_data_scan_use_case.get_database_domain"
    )
    def test_get_data_scan_use_case_valid_input(self, mock_get_database_domain):
        """
        Prueba cuando la entrada es inválida.
        """
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_id.return_value = None
        mock_repo.get_scan_data_by_id.return_value = None
        mock_get_database_domain.return_value = mock_repo

        data_id = ""
        use_case = GetDataScanUseCase()

        with self.assertRaises(HTTPException) as context:
            use_case.get_data_scan_use_case(data_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 400)

    @patch(
        "api.application.use_cases.databasec.get_data_scan_use_case.get_database_domain"
    )
    def test_get_data_scan_use_case_database_not_found(self, mock_get_database_domain):
        """
        Prueba cuando la base de datos no se encuentra.
        """
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_id.return_value = None
        mock_repo.get_scan_data_by_id.return_value = None
        mock_get_database_domain.return_value = mock_repo

        data_id = "id_id"
        use_case = GetDataScanUseCase()

        with self.assertRaises(HTTPException) as context:
            use_case.get_data_scan_use_case(data_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 404)

    @patch(
        "api.application.use_cases.databasec.get_data_scan_use_case.get_database_domain"
    )
    def test_get_data_scan_use_case_order_data_scan(self, mock_get_database_domain):
        """
        Configura el mock para simular la respuesta de la base de datos
        """
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
        mock_repo.get_scan_data_by_id.return_value = [
            ScanDatabaseById(
                domain_id="domain_id",
                domain_name="domain_name",
                table_name="table_name",
                detail_column_name="detail_column_name",
                type_description="type_description",
            )
        ]

        mock_get_database_domain.return_value = mock_repo
        data_id = "id_id"
        use_case = GetDataScanUseCase()
        result = use_case.get_data_scan_use_case(data_id)

        result_expect = [
            GetScanDomain(
                nameDatabase="domain_name",
                listTable=[
                    GetScanTable(
                        nameTable="table_name",
                        listColum=[
                            GetScanTableDetail(
                                nameColumn="detail_column_name",
                                typeIdentified="type_description",
                            )
                        ],
                    )
                ],
            )
        ]
        self.assertEqual(result, result_expect)
