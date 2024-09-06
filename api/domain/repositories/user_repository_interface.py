from abc import ABC, abstractmethod
from api.domain.entities.User import UserEntity


class UserRepositoryInterface(ABC):

    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_id(self, id: int) -> UserEntity:
        pass
