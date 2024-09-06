import unittest
from unittest.mock import MagicMock, patch
import uuid

from fastapi import HTTPException
from api.application.models.databasec.save_model import SaveDatabaseModel
from api.application.use_cases.databasec.save_database_use_case import DatabaseUseCase
from api.domain.entities.databaseC import DatabaseEntity
from api.test.mocks.encrypt_use_case_mock import encrypt_text_mock_use_case


class TestSaveDatabaseUseCase(unittest.TestCase):

    @patch(
        "api.application.use_cases.databasec.save_database_use_case.EncryptUseCase",
        new_callable=encrypt_text_mock_use_case,
    )
    @patch(
        "api.application.use_cases.databasec.save_database_use_case.get_database_domain"
    )
    def test_save_data_use_case_successful_save(
        self, mock_get_database_domain, mock_encrypt_use_case
    ):
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_host_port.return_value = None
        mock_repo.create_databasec.return_value = None
        mock_get_database_domain.return_value = mock_repo

        database_data = SaveDatabaseModel(
            host="host", port=1234, username="user", password="pss"
        )
        user_id = 1
        use_case = DatabaseUseCase()
        use_case.save_data_use_case(database_data, user_id)

        mock_repo.create_databasec.assert_called_once()

    @patch(
        "api.application.use_cases.databasec.save_database_use_case.EncryptUseCase",
        new_callable=encrypt_text_mock_use_case,
    )
    @patch(
        "api.application.use_cases.databasec.save_database_use_case.get_database_domain"
    )
    def test_save_data_use_case_incorrect_input(
        self, mock_get_database_domain, mock_encrypt_use_case
    ):
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_host_port.return_value = None
        mock_repo.create_databasec.return_value = None
        mock_get_database_domain.return_value = mock_repo

        database_data = SaveDatabaseModel(host="", port=0, username="", password="")
        user_id = 1
        use_case = DatabaseUseCase()

        with self.assertRaises(HTTPException) as context:
            use_case.save_data_use_case(database_data, user_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 400)
        mock_repo.create_databasec.assert_not_called()

    @patch(
        "api.application.use_cases.databasec.save_database_use_case.EncryptUseCase",
        new_callable=encrypt_text_mock_use_case,
    )
    @patch(
        "api.application.use_cases.databasec.save_database_use_case.get_database_domain"
    )
    def test_save_data_use_case_database_already_exists(
        self, mock_get_database_domain, mock_encrypt_use_case
    ):
        mock_repo = MagicMock()
        mock_repo.get_databasec_by_host_port.return_value = DatabaseEntity(
            id=uuid.uuid4(),
            host="nuevo",
            port=1234,
            username="username",
            password="password",
            user_id=2,
        )
        mock_repo.create_databasec.return_value = None
        mock_get_database_domain.return_value = mock_repo

        database_data = SaveDatabaseModel(
            host="host", port=1234, username="user", password="name"
        )
        user_id = 1
        use_case = DatabaseUseCase()

        with self.assertRaises(HTTPException) as context:
            use_case.save_data_use_case(database_data, user_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 404)
        mock_repo.create_databasec.assert_not_called()
