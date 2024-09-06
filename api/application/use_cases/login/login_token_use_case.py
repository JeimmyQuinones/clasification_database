from fastapi import HTTPException
from api.domain.repositories.user_repository_interface import UserRepositoryInterface
from api.application.config.dependencies.domain_dependencies import get_user_domain
from api.application.use_cases.Hash.hash_use_case import HashUseCase
from api.application.models.users.user_create_model import UserCreate
from api.application.models.login.token_model import Token

from datetime import timedelta
from api.application.config.config import settings


class LoginTokenUseCase:

    dominio: UserRepositoryInterface

    def __init__(self) -> None:
        super().__init__()
        self.dominio = get_user_domain()

    def login_token_case(self, user_request: UserCreate) -> dict:
        """
        Valida las credenciales del usuario y
        genera un token de acceso si son correctas.
        Lanza una excepción si el usuario no existe o la contraseña es incorrecta.
        """
        user = self.dominio.get_user_by_username(user_request.username)
        if user is None:
            raise HTTPException(status_code=404, detail="Invalid User")
        elif HashUseCase.verify_password(user_request.password, user.password):
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = HashUseCase.create_access_token(
                user.id, expires_delta=access_token_expires
            )
            return Token(access_token=access_token)

        raise HTTPException(status_code=401, detail="Incorrect password")
