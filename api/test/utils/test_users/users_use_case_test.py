import unittest
from unittest.mock import MagicMock, patch
from api.application.use_cases.Users.create_user_use_case import CreateUserUseCase
from api.application.models.users.user_create_model import UserCreate
from api.domain.entities.User import UserEntity
from api.test.mocks.hash_use_case_mock import get_password_mock_hash_use_case


class TestCreateUserUseCase(unittest.TestCase):

    @patch(
        "api.application.use_cases.Users.create_user_use_case.HashUseCase",
        new_callable=get_password_mock_hash_use_case,
    )
    @patch("api.application.use_cases.Users.create_user_use_case.get_user_domain")
    def test_create_user_case_user_does_not_exist(
        self, mock_get_user_domain, mock_hash_use_case
    ):

        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_username.return_value = None
        mock_user_repo.create_user.return_value = None
        mock_get_user_domain.return_value = mock_user_repo

        use_case = CreateUserUseCase()
        user_request = UserCreate(username="test_user", password="test_password")
        result = use_case.create_user_case(user_request)

        self.assertTrue(result)
        # Verifica que se llamó a los métodos esperados
        mock_user_repo.get_user_by_username.assert_called_once_with("test_user")
        mock_user_repo.create_user.assert_called_once()
        mock_hash_use_case.get_password_hash.assert_called_once_with("test_password")

    @patch(
        "api.application.use_cases.Users.create_user_use_case.HashUseCase",
        new_callable=get_password_mock_hash_use_case,
    )
    @patch("api.application.use_cases.Users.create_user_use_case.get_user_domain")
    def test_create_user_case_user_exists(
        self, mock_get_user_domain, mock_hash_use_case
    ):
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_username.return_value = UserEntity(
            id=1, username="hash_user", password="hash_password"
        )
        mock_user_repo.create_user.return_value = None
        mock_get_user_domain.return_value = mock_user_repo

        use_case = CreateUserUseCase()
        user_request = UserCreate(username="test_user", password="test_password")
        result = use_case.create_user_case(user_request)

        self.assertFalse(result)

        mock_user_repo.create_user.assert_not_called()

    @patch(
        "api.application.use_cases.Users.create_user_use_case.HashUseCase",
        new_callable=get_password_mock_hash_use_case,
    )
    @patch("api.application.use_cases.Users.create_user_use_case.get_user_domain")
    def test_create_user_case_password_hashing(
        self, mock_get_user_domain, mock_hash_use_case
    ):
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_username.return_value = None
        mock_user_repo.create_user.return_value = None
        mock_get_user_domain.return_value = mock_user_repo

        use_case = CreateUserUseCase()
        user_request = UserCreate(username="test_user", password="test_password")
        use_case.create_user_case(user_request)
        # Verifica que la contraseña fue hasheada correctamente
        mock_hash_use_case.get_password_hash.assert_called_once_with("test_password")
