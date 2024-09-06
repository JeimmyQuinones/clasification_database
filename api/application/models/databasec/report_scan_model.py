from datetime import datetime
from typing import List
from pydantic import BaseModel


class LastScantableDetail(BaseModel):
    name_table: str
    total_columns: int
    total_classified_columns: int
    porcentage_classified_columns: float


class LastScanDetail(BaseModel):
    name_scheme: str | None = None
    list_tables_detail: List[LastScantableDetail] = []


class ClassifiedScanModel(BaseModel):
    type_name: str
    total_columns: int
    percentage: float


class HistoricalScanModel(BaseModel):
    version_scan: int
    date_scan: datetime | None
    total_schemes_scan: int
    total_tables_scan: int
    total_columns_scan: int
    total_columns_classified_scan: int
    percentage_classified_scan: float | None = None
    classified_by_type_list_scan: List[ClassifiedScanModel] = []


class ReportScanModel(BaseModel):
    historical_scan: List[HistoricalScanModel] = []
    last_scan_detail: List[LastScanDetail] = []
