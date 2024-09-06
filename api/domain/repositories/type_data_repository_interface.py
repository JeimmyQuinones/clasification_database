from abc import ABC, abstractmethod

from api.domain.entities.type_data import TypeDataEntity


class TypeDataRepositoryInterface(ABC):

    @abstractmethod
    def get_all_type_data(self) -> TypeDataEntity:
        pass
