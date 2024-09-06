from abc import ABC, abstractmethod

from api.application.models.users.user_create_model import UserCreate


class UserServiceInterface(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate):
        pass
