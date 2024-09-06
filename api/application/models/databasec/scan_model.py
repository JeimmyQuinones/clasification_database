from pydantic import BaseModel


class ScanDatabaseModel(BaseModel):
    id: str


class TypeDataBaseModel(BaseModel):
    id: int
    name: str
    alias: list[str]
