import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from api.application.config.config import settings

# from typing import Any


class HashUseCase:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = settings.ALGORITHM

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con la contraseña hasheada."""
        return HashUseCase.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Devuelve el hash de la contraseña dada."""
        return HashUseCase.pwd_context.hash(password)

    @staticmethod
    def create_access_token(subject: str, expires_delta: timedelta) -> str:
        """Crea un token de acceso con un tiempo de expiración."""
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=HashUseCase.ALGORITHM
        )
        return encoded_jwt
