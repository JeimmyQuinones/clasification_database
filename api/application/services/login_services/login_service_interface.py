from abc import ABC, abstractmethod

from api.application.models.users.user_create_model import UserCreate


class LoginServiceInterface(ABC):
    @abstractmethod
    def login_token(self, user: UserCreate):
        pass
