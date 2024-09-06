from abc import ABC, abstractmethod
from typing import List

from api.domain.entities.scan_table_info import GetTableInfoEntity


class ScanDatabaseRepositoryInterface(ABC):

    @abstractmethod
    def get_info_by_database(self, url: str) -> List[str]:
        pass

    @abstractmethod
    def get_database_info(self, url: str, database: str) -> List[GetTableInfoEntity]:
        pass
