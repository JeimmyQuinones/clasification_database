from api.domain.entities.User import UserEntity
from api.domain.repositories.user_repository_interface import UserRepositoryInterface
from api.application.config.dependencies.domain_dependencies import get_user_domain
from api.application.use_cases.Hash.hash_use_case import HashUseCase
from api.application.models.users.user_create_model import UserCreate


class CreateUserUseCase:

    dominio: UserRepositoryInterface

    def __init__(self) -> None:
        super().__init__()
        self.dominio = get_user_domain()

    def create_user_case(self, user_request: UserCreate) -> dict:
        """
        Crea un nuevo usuario si el nombre de usuario no existe.
        """
        state_creation: bool = False
        user_name = self.dominio.get_user_by_username(user_request.username)
        if user_name is None:
            user = UserEntity(
                username=user_request.username,
                password=HashUseCase.get_password_hash(user_request.password),
            )
            self.dominio.create_user(user)
            state_creation = True
        return state_creation
