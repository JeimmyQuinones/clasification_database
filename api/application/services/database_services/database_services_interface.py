from abc import ABC, abstractmethod

from api.application.models.databasec.save_model import SaveDatabaseModel
from api.application.models.databasec.scan_model import ScanDatabaseModel


class DatabaseServiceInterface(ABC):
    @abstractmethod
    def Save_database_info(self, data: SaveDatabaseModel, user_id: int):
        pass

    @abstractmethod
    def scan_database_by_id(self, scan_data: ScanDatabaseModel):
        pass

    @abstractmethod
    def get_scan_database_by_id(self, id: str):
        pass

    @abstractmethod
    def report_scan_database_by_id(self, id: str):
        pass
