from typing import Any, Optional

from pydantic.main import BaseModel


class RequestParams(BaseModel):
    skip: int
    limit: int
    order_by: Any


class ReportParams(BaseModel):
    skip: int
    limit: int
    order_by: Any
    domain_id: Optional[int] = None
    post_id: Optional[int] = None

    class Config:
        orm_mode=True