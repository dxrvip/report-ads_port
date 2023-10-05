from typing import Any, Optional, Union
from datetime import date
from pydantic.main import BaseModel


class RequestParams(BaseModel):
    skip: int
    limit: int
    order_by: Any


class Filters(BaseModel):
    domain_id: Optional[int]
    create_time: Optional[date]
    create: Optional[date]
    slug: Optional[str]
    id: Optional[int]
    promotion: Optional[int]
    post_id: Optional[int]
    site_id: Optional[int]


class ReportParams(BaseModel):
    skip: int
    limit: int
    order_by: Any
    filters: Filters

    class Config:
        orm_mode=True

