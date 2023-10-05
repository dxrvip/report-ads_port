import json
from typing import Annotated, Callable, Optional, Type
 
from fastapi import Depends, HTTPException, Query
from sqlalchemy import UnaryExpression, asc, desc

from app.db import Base
from app.models.item import Item
from app.models.domain import Domain
from app.models.report import ReportPost, Post, Taboola, BrowserInfo
from app.schemas.request_params import RequestParams, ReportParams


def parse_react_admin_params(model: Type[Base]) -> Callable:
    """解析来自react-admin请求的排序和范围参数"""

    def inner(
        sort_: Optional[str] = Query(
            None,
            alias="sort",
            description='Format: `["field_name", "direction"]`',
            example='["id", "ASC"]',
        ),
        range_: Optional[str] = Query(
            None,
            alias="range",
            description="Format: `[start, end]`",
            example="[0, 10]",
        ),
    ) -> RequestParams:
        skip, limit = 0, 10
        if range_:
            start, end = json.loads(range_)
            skip, limit = start, (end - start + 1)

        order_by: UnaryExpression = desc(model.id)
        if sort_:
            sort_column, sort_order = json.loads(sort_)
            if sort_order.lower() == "asc":
                direction = asc
            elif sort_order.lower() == "desc":
                direction = desc
            else:
                raise HTTPException(400, f"Invalid sort direction {sort_order}")
            order_by = direction(model.__table__.c[sort_column])

        return RequestParams(skip=skip, limit=limit, order_by=order_by)

    return inner

def parse_react_post_params(model: Type[Base]) -> Callable:
    """解析来自react-admin统计请求的排序和范围参数"""

    def inner(
        sort_: Optional[str] = Query(
            None,
            alias="sort",
            description='Format: `["field_name", "direction"]`',
            example='["id", "ASC"]',
        ),
        range_: Optional[str] = Query(
            None,
            alias="range",
            description="Format: `[start, end]`",
            example="[0, 10]",
        ),
        filter_: Optional[str] = Query(
            ...,
            alias="filter",
            description="统计数据字段",
            example='["domain_id", "post_id"]'
        )
    ) -> RequestParams:
        skip, limit = 0, 10
        if filter_:
            filter_dict = json.loads(filter_)
        if range_:
            start, end = json.loads(range_)
            skip, limit = start, (end - start + 1)

        order_by: UnaryExpression = desc(model.id)
        if sort_:
            sort_column, sort_order = json.loads(sort_)
            if sort_order.lower() == "asc":
                direction = asc
            elif sort_order.lower() == "desc":
                direction = desc
            else:
                raise HTTPException(400, f"Invalid sort direction {sort_order}")
            if model.__dict__.get(sort_column):
                order_by = direction(model.__table__.c[sort_column])
            else:
                order_by = direction(sort_column)
        return ReportParams(filters=filter_dict, skip=skip, limit=limit, order_by=order_by)

    return inner

ItemRequestParams = Annotated[RequestParams, Depends(parse_react_admin_params(Item))]
DomainRequestParams = Annotated[RequestParams, Depends(parse_react_post_params(Domain))]



PostRequestParams = Annotated[ReportParams, Depends(parse_react_post_params(Post))]
TaboolaRequestParams = Annotated[ReportParams, Depends(parse_react_post_params(Taboola))]
BrowserRequestParams = Annotated[ReportParams, Depends(parse_react_post_params(BrowserInfo))]
PostReportRequestParams = Annotated[ReportParams, Depends(parse_react_post_params(ReportPost))]