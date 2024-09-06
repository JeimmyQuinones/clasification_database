from api.application.services.login_services.login_service_interface import (
    LoginServiceInterface,
)
from api.application.models.users.user_create_model import UserCreate
from typing import Dict
from api.application.use_cases.login.login_token_use_case import LoginTokenUseCase


class LoginServiceImpl(LoginServiceInterface):

    def __init__(
        self,
        login_token_use_case: LoginTokenUseCase,
    ) -> None:
        self.login_token_use_case = login_token_use_case

    def login_token(self, user_request: UserCreate) -> Dict[str, str]:
        login = self.login_token_use_case.login_token_case(user_request)
        return login
