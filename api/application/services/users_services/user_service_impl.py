from api.application.services.users_services.services_interface import (
    UserServiceInterface,
)
from api.application.models.users.user_create_model import UserCreate
from typing import Dict
from api.application.use_cases.Users.create_user_use_case import CreateUserUseCase


class UserServiceImpl(UserServiceInterface):

    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
    ) -> None:
        self.create_user_use_case = create_user_use_case

    def create_user(self, user_request: UserCreate) -> Dict[str, str]:
        creation_state = self.create_user_use_case.create_user_case(user_request)
        return creation_state
