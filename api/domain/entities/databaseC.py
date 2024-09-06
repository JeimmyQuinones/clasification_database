from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class DatabaseEntity(BaseModel):
    id: UUID | None = None
    host: str
    port: int
    username: str
    password: str
    user_id: int | None = None
    date_scan: datetime | None = None
    lates_scan_version: int | None = None


class ScanDatabaseById(BaseModel):
    domain_id: str
    domain_name: str
    table_name: str
    detail_column_name: str
    type_description: str
