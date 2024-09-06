from unittest.mock import MagicMock


def get_password_mock_hash_use_case():
    """
    Crea un mock para simular la creacion de un hash de la contraseña.
    """
    mock_item = MagicMock()
    mock_item.get_password_hash.return_value = "hashed_password"
    return mock_item


def get_verify_password_create_token_mock(is_password_correct=False):
    """
    Crea un mock que verifica si una contraseña es correcta o no.
    """

    mock_item = MagicMock()
    mock_item.create_access_token.return_value = "token_password"
    if is_password_correct:
        mock_item.verify_password.return_value = True
    else:
        mock_item.verify_password.return_value = False
    return mock_item


def get_create_access_token_mock_hash_use_case():
    """
    Crea un mock para simular la creacion de un token .
    """
    mock_item = MagicMock()
    return mock_item
