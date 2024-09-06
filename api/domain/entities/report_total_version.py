from datetime import datetime
from pydantic import BaseModel


class ReportTotalVersionEntity(BaseModel):
    total_schemes: int | None = None
    total_tablas: int | None = None
    total_columnas: int | None = None
    total_clasificadas: int | None = None
    version_scan: int | None = None
    date_scan: datetime | None = None


class ReportTypeVersionEntity(BaseModel):
    name_tipo: str | None = None
    total_columnas: int | None = None
    version_scan: int | None = None


class ReportDetailVersionEntity(BaseModel):
    domain_name: str | None = None
    domain_id: str | None = None
    columns: int | None = None
    total_clasification: int | None = None
    table_name: str | None = None
