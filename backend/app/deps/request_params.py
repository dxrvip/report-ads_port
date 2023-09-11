import json
from typing import Annotated, Callable, Optional, Type
 
from fastapi import Depends, HTTPException, Query
from sqlalchemy import UnaryExpression, asc, desc

from app.db import Base
from app.models.item import Item
from app.models.domain import Domain
from app.models.report import ReportPost, Post, Taboola, BrowserInfo
from app.schemas.request_params import RequestParams, PostParams


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
        filter_: Optional[str] = Query(
            None,
            alias="filter",
            description="Format: `[post_id]`",
            example='["domain_id"]'
        )
    ) -> RequestParams:
        skip, limit = 0, 10
        if filter_:
            record_id = json.loads(filter_).get('record_id')
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

        return PostParams(skip=skip, limit=limit, order_by=order_by, record_id=record_id)

    return inner

ItemRequestParams = Annotated[RequestParams, Depends(parse_react_admin_params(Item))]
DomainRequestParams = Annotated[RequestParams, Depends(parse_react_admin_params(Domain))]
ReportRequestParams = Annotated[RequestParams, Depends(parse_react_admin_params(ReportPost))]
PostRequestParams = Annotated[PostParams, Depends(parse_react_post_params(Post))]
TaboolaRequestParams = Annotated[PostParams, Depends(parse_react_post_params(Taboola))]
BrowserRequestParams = Annotated[PostParams, Depends(parse_react_post_params(BrowserInfo))]
PostReportRequestParams = Annotated[RequestParams, Depends(parse_react_post_params(ReportPost))]