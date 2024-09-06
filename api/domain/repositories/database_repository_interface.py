from abc import ABC, abstractmethod
from typing import List
from api.domain.entities.databaseC import DatabaseEntity
from api.domain.entities.scan_table_info import (
    ScanDetailTableEntity,
    ScanDomainEntity,
    ScanTableEntity,
)


class DatabaseRepositoryInterface(ABC):

    @abstractmethod
    def create_databasec(self, user: DatabaseEntity) -> DatabaseEntity:
        pass

    @abstractmethod
    def get_databasec_by_host_port(self, host: str, port: str) -> DatabaseEntity:
        pass

    @abstractmethod
    def get_databasec_by_id(self, id: str) -> DatabaseEntity:
        pass

    @abstractmethod
    def Add_domain_scan_list(self, data: List[ScanDomainEntity]) -> None:
        pass

    @abstractmethod
    def Add_tables_scan_list(self, data: List[ScanTableEntity]) -> None:
        pass

    @abstractmethod
    def Add_tables_detail_scan_list(self, data: List[ScanDetailTableEntity]) -> None:
        pass

    @abstractmethod
    def get_scan_data_by_id(self, id: str, last_version: int) -> None:
        pass

    @abstractmethod
    def get_report_totals_info_version(self, id: str) -> None:
        pass

    @abstractmethod
    def get_report_types_info(self, id: str) -> None:
        pass

    @abstractmethod
    def get_report_by_version_detail(self, id: str, version: int) -> None:
        pass
