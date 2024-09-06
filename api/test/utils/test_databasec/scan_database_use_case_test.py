from datetime import datetime
from typing import List
import unittest
from unittest.mock import MagicMock, patch
import uuid

from fastapi import HTTPException
from api.application.models.databasec.scan_model import ScanDatabaseModel
from api.application.use_cases.databasec.scan_use_case import ScanUseCase
from api.domain.entities.databaseC import DatabaseEntity
from api.domain.entities.scan_table_info import GetDomainInfoEntity, GetTableInfoEntity
from api.domain.entities.type_data import TypeDataEntity
from api.test.mocks.encrypt_use_case_mock import get_decrypt_text_mock_use_case


class TestScanDatabaseUseCase(unittest.TestCase):

    @patch(
        "api.application.use_cases.databasec.scan_use_case.EncryptUseCase",
        new_callable=get_decrypt_text_mock_use_case,
    )
    @patch("api.application.use_cases.databasec.scan_use_case.get_database_domain")
    @patch("api.application.use_cases.databasec.scan_use_case.get_type_data_domain")
    @patch("api.application.use_cases.databasec.scan_use_case.get_scan_database_domain")
    def test_scan_use_case_successful_scan(
        self,
        mock_get_scan_domain,
        mock_get_type_domain,
        mock_get_database_domain,
        mock_encrypt_use_case,
    ):
        mock_repo_scan = MagicMock()
        mock_repo_scan.get_database_info.return_value = GetDomainInfoEntity(
            nameDatabase="nombre",
            table_list=[
                GetTableInfoEntity(name_table="tabla", colum_list=["col1", "col2"]),
                GetTableInfoEntity(name_table="tabla2", colum_list=["col1", "col2"]),
            ],
        )
        mock_repo_scan.get_info_by_database.return_value = [
            "database1",
            "database2",
        ]
        mock_get_scan_domain.return_value = mock_repo_scan

        mock_repo_database = MagicMock()
        mock_repo_database.get_databasec_by_id.return_value = DatabaseEntity(
            id=uuid.uuid4(),
            host="db_data.host",
            port=1234,
            username="db_data.username",
            password="db_data.password",
            user_id=1,
            date_scan=datetime.now(),
            lates_scan_version=1,
        )
        mock_repo_database.Add_domain_scan_list.return_value = None
        mock_repo_database.Add_tables_scan_list.return_value = None
        mock_repo_database.Add_tables_detail_scan_list.return_value = None
        mock_repo_database.Update_databasec.return_value = None
        mock_get_database_domain.return_value = mock_repo_database

        mock_repo_type = MagicMock()
        mock_repo_type.get_all_type_data.return_value = [
            TypeDataEntity(id=1, name="item.name", alias="na"),
            TypeDataEntity(id=2, name="N/A", alias="ff"),
        ]

        mock_get_type_domain.return_value = mock_repo_type

        database_id = ScanDatabaseModel(id="id_id")

        use_case = ScanUseCase()
        use_case.scan_use_case(database_id)

        mock_repo_database.Add_domain_scan_list.assert_called_once()
        mock_repo_database.Add_tables_scan_list.assert_called_once()
        mock_repo_database.Add_tables_detail_scan_list.assert_called_once()
        mock_repo_database.Update_databasec.assert_called_once()

    @patch(
        "api.application.use_cases.databasec.scan_use_case.EncryptUseCase",
        new_callable=get_decrypt_text_mock_use_case,
    )
    @patch("api.application.use_cases.databasec.scan_use_case.get_database_domain")
    @patch("api.application.use_cases.databasec.scan_use_case.get_type_data_domain")
    @patch("api.application.use_cases.databasec.scan_use_case.get_scan_database_domain")
    def test_scan_use_case_id_not_found(
        self,
        mock_get_scan_domain,
        mock_get_type_domain,
        mock_get_database_domain,
        mock_encrypt_use_case,
    ):
        mock_repo_scan = MagicMock()
        mock_repo_scan.get_database_info.return_value = None
        mock_repo_scan.get_info_by_database.return_value = None
        mock_get_scan_domain.return_value = mock_repo_scan

        mock_repo_database = MagicMock()
        mock_repo_database.get_databasec_by_id.return_value = None
        mock_repo_database.Add_domain_scan_list.return_value = None
        mock_repo_database.Add_tables_scan_list.return_value = None
        mock_repo_database.Add_tables_detail_scan_list.return_value = None
        mock_repo_database.Update_databasec.return_value = None
        mock_get_database_domain.return_value = mock_repo_database

        mock_repo_type = MagicMock()
        mock_repo_type.get_all_type_data.return_value = [
            TypeDataEntity(id=1, name="item.name", alias="na"),
            TypeDataEntity(id=2, name="N/A", alias="ff"),
        ]
        mock_get_type_domain.return_value = mock_repo_type

        database_id = ScanDatabaseModel(id="id_id")

        use_case = ScanUseCase()
        with self.assertRaises(HTTPException) as context:
            use_case.scan_use_case(database_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 404)

        mock_repo_database.Add_domain_scan_list.assert_not_called()
        mock_repo_database.Add_tables_scan_list.assert_not_called()
        mock_repo_database.Add_tables_detail_scan_list.assert_not_called()
        mock_repo_database.Update_databasec.assert_not_called()

    @patch(
        "api.application.use_cases.databasec.scan_use_case.EncryptUseCase",
        new_callable=get_decrypt_text_mock_use_case,
    )
    @patch("api.application.use_cases.databasec.scan_use_case.get_database_domain")
    @patch("api.application.use_cases.databasec.scan_use_case.get_type_data_domain")
    @patch("api.application.use_cases.databasec.scan_use_case.get_scan_database_domain")
    def test_scan_use_case_input_invalid(
        self,
        mock_get_scan_domain,
        mock_get_type_domain,
        mock_get_database_domain,
        mock_encrypt_use_case,
    ):
        mock_repo_scan = MagicMock()
        mock_repo_scan.get_database_info.return_value = None
        mock_repo_scan.get_info_by_database.return_value = None
        mock_get_scan_domain.return_value = mock_repo_scan

        mock_repo_database = MagicMock()
        mock_repo_database.get_databasec_by_id.return_value = None
        mock_repo_database.Add_domain_scan_list.return_value = None
        mock_repo_database.Add_tables_scan_list.return_value = None
        mock_repo_database.Add_tables_detail_scan_list.return_value = None
        mock_repo_database.Update_databasec.return_value = None
        mock_get_database_domain.return_value = mock_repo_database

        mock_repo_type = MagicMock()
        mock_repo_type.get_all_type_data.return_value = [
            TypeDataEntity(id=1, name="item.name", alias="na"),
            TypeDataEntity(id=2, name="N/A", alias="ff"),
        ]
        mock_get_type_domain.return_value = mock_repo_type

        database_id = ScanDatabaseModel(id="")

        use_case = ScanUseCase()
        with self.assertRaises(HTTPException) as context:
            use_case.scan_use_case(database_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 400)

        mock_repo_database.Add_domain_scan_list.assert_not_called()
        mock_repo_database.Add_tables_scan_list.assert_not_called()
        mock_repo_database.Add_tables_detail_scan_list.assert_not_called()
        mock_repo_database.Update_databasec.assert_not_called()
