import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from api.application.models.login.token_model import Token
from api.application.models.users.user_create_model import UserCreate
from api.application.use_cases.login.login_token_use_case import LoginTokenUseCase
from api.domain.entities.User import UserEntity
from api.test.mocks.hash_use_case_mock import get_verify_password_create_token_mock


class TestLoginTokenUseCase(unittest.TestCase):

    @patch(
        "api.application.use_cases.login.login_token_use_case.HashUseCase",
        new_callable=lambda: get_verify_password_create_token_mock(True),
    )
    @patch("api.application.use_cases.login.login_token_use_case.get_user_domain")
    def test_login_token_case_user_not_found(
        self, mock_get_user_domain, mock_hash_use_case
    ):

        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_username.return_value = None
        mock_get_user_domain.return_value = mock_user_repo

        use_case = LoginTokenUseCase()
        user = UserCreate(username="user_text", password="pass_text")

        # Ejecuta el método y verifica que se lanza una excepción
        with self.assertRaises(HTTPException) as context:
            use_case.login_token_case(user)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 404)

    @patch(
        "api.application.use_cases.login.login_token_use_case.HashUseCase",
        new_callable=lambda: get_verify_password_create_token_mock(False),
    )
    @patch("api.application.use_cases.login.login_token_use_case.get_user_domain")
    def test_login_token_case_incorrect_password(
        self, mock_get_user_domain, mock_hash_use_case
    ):

        mock_user_repo = MagicMock()
        user_response = UserEntity(id=1, username="hash_user", password="hash_password")
        mock_user_repo.get_user_by_username.return_value = user_response
        mock_get_user_domain.return_value = mock_user_repo

        use_case = LoginTokenUseCase()
        user = UserCreate(username="user_text", password="pass_text")

        # Ejecuta el método y verifica que se lanza una excepción
        with self.assertRaises(HTTPException) as context:
            use_case.login_token_case(user)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 401)

    @patch(
        "api.application.use_cases.login.login_token_use_case.HashUseCase",
        new_callable=lambda: get_verify_password_create_token_mock(True),
    )
    @patch("api.application.use_cases.login.login_token_use_case.get_user_domain")
    def test_login_token_case_successful_login(
        self, mock_get_user_domain, mock_hash_use_case
    ):

        mock_user_repo = MagicMock()
        user_response = UserEntity(id=1, username="hash_user", password="hash_password")
        mock_user_repo.get_user_by_username.return_value = user_response
        mock_get_user_domain.return_value = mock_user_repo

        use_case = LoginTokenUseCase()
        user = UserCreate(username="user_text", password="pass_text")

        hash_pasword = Token(access_token="token_password")
        result = use_case.login_token_case(user)
        # Verifica que el resultado es el usuario esperado
        self.assertEqual(result, hash_pasword)
