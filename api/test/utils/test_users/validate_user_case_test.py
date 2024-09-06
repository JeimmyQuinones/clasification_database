import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from api.application.use_cases.Users.validate_user_use_case import ValidateUserUseCase
from api.domain.entities.User import UserEntity


class TestValidateUserUseCase(unittest.TestCase):

    @patch("api.application.use_cases.Users.validate_user_use_case.get_user_domain")
    def test_validate_user_case_user_exists(self, mock_get_user_domain):

        mock_user_repo = MagicMock()
        expected_user = UserEntity(id=1, username="prueba", password="prueba")
        mock_user_repo.get_user_by_id.return_value = expected_user
        mock_get_user_domain.return_value = mock_user_repo

        use_case = ValidateUserUseCase()
        user_id = 1
        result = use_case.validate_user_case(user_id)

        # Verifica que el resultado es el usuario esperado
        self.assertEqual(result, expected_user)
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id)

    @patch("api.application.use_cases.Users.validate_user_use_case.get_user_domain")
    def test_validate_user_case_user_does_not_exist(self, mock_get_user_domain):

        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_id.return_value = None
        mock_get_user_domain.return_value = mock_user_repo

        use_case = ValidateUserUseCase()
        user_id = 1

        # Ejecuta el método y verifica que se lanza una excepción
        with self.assertRaises(HTTPException) as context:
            use_case.validate_user_case(user_id)

        # Verifica el tipo y contenido de la excepción
        self.assertEqual(type(context.exception), HTTPException)
        self.assertEqual(context.exception.status_code, 404)
