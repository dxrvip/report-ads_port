from typing import Any

from pydantic.main import BaseModel


class RequestParams(BaseModel):
    skip: int
    limit: int
    order_by: Any


class PostParams(BaseModel):
    skip: int
    limit: int
    order_by: Any
    record_id: int