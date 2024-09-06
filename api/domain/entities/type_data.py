from pydantic import BaseModel


class TypeDataEntity(BaseModel):
    id: int
    name: str
    alias: str
