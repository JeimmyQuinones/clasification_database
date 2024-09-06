from fastapi import HTTPException
from api.domain.repositories.user_repository_interface import UserRepositoryInterface
from api.application.config.dependencies.domain_dependencies import get_user_domain


class ValidateUserUseCase:

    dominio: UserRepositoryInterface

    def __init__(self) -> None:
        super().__init__()
        self.dominio = get_user_domain()

    def validate_user_case(self, id: int) -> dict:
        """
        Obtiene un usuario por ID. Lanza una excepción si el usuario no se encuentra.
        """
        user = self.dominio.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
