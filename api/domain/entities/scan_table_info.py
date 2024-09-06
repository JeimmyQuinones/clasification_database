from typing import List
from pydantic import BaseModel


class GetTableInfoEntity(BaseModel):
    name_table: str
    colum_list: List[str]


class GetDomainInfoEntity(BaseModel):
    nameDatabase: str
    table_list: List[GetTableInfoEntity]


class ScanDetailTableEntity(BaseModel):
    id: str | None = None
    table_id: str
    nameColumn: str
    typeIdentified_id: int


class ScanTableEntity(BaseModel):
    id: str | None = None
    domain_id: str
    name: str


class ScanDomainEntity(BaseModel):
    id: str | None = None
    database_id: str
    version: int
    name: str


class ScanEntiryList(BaseModel):
    domain_list: List[ScanDomainEntity] = []
    table_list: List[ScanTableEntity] = []
    detail_table_list: List[ScanDetailTableEntity] = []
