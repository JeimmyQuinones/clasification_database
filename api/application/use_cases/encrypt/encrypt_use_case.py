from api.application.config.config import settings
from cryptography.fernet import Fernet

# from typing import Any


class EncryptUseCase:
    key = settings.ENCRYPTKEY.encode()
    fernet = Fernet(key)

    @staticmethod
    def encrypt_text(text: str) -> str:
        """Encripta un texto ."""
        return EncryptUseCase.fernet.encrypt(text.encode()).decode()

    @staticmethod
    def decrypt_text(text: str) -> str:
        """Desencripta un texto encriptado."""
        return EncryptUseCase.fernet.decrypt(text.encode()).decode()
