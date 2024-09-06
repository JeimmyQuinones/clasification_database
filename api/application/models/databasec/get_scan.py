from typing import List
from pydantic import BaseModel


class GetScanTableDetail(BaseModel):
    nameColumn: str
    typeIdentified: str


class GetScanTable(BaseModel):
    nameTable: str
    listColum: List[GetScanTableDetail] = []


class GetScanDomain(BaseModel):
    nameDatabase: str
    listTable: List[GetScanTable] = []
