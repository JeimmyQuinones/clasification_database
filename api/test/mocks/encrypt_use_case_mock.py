from unittest.mock import MagicMock


def encrypt_text_mock_use_case():
    """
    Crea un mock para simular la encriptación de texto.
    """
    mock_item = MagicMock()
    mock_item.encrypt_text.return_value = "encrypt"
    return mock_item


def get_decrypt_text_mock_use_case():
    """
    Crea un mock para simular la desencriptación de texto.
    """
    mock_item = MagicMock()
    mock_item.decrypt_text.return_value = "decrypt"

    return mock_item
