from fastapi import APIRouter, Query, HTTPException
from typing import List, Any, Optional
from app.schemas.msg import Msg
from urllib.parse import urlparse, parse_qs
from sqlalchemy import distinct, select, func, cast, DATE
from starlette.responses import Response
from app.schemas.post import (
    PostListReport as SchemasPost,
    ReportPost as SchemasReportPost,
)
from app.schemas.report import ResultBrowserInfo as SchemasBrowser
from app.deps.users import CurrentUser
from app.deps.db import CurrentAsyncSession
from app.deps.request_params import (
    PostRequestParams,
    TaboolaRequestParams,
    BrowserRequestParams,
    PostReportRequestParams,
)
from app.schemas.report import Report as ReportSchema
from app.crud import report as report_crud
from app.crud import post as crud
from app.models.report import ItemStatus, Post, Taboola, BrowserInfo, ReportPost
from app.utils.taboola_api import TaboolaApi
from app.schemas import taboola as schemas_taboola

router = APIRouter(prefix="/list")


#
@router.get("/post", response_model=List[SchemasPost], status_code=201)
async def get_posts(
    response: Response,
    session: CurrentAsyncSession,
    request_params: PostRequestParams,
    user: CurrentUser,
) -> Any:
    filters = request_params.filters

    stmt = select(func.count(Post.id)).filter_by(
        **filters.dict(exclude_unset=True, exclude={"create_time"})
    )
    # print(stmt)
    if filters.create_time:
        stmt = stmt.filter(
            cast(Post.create_time, DATE) == cast(filters.create_time, DATE)
        )
    # print(stmt)
    total = await session.scalar(stmt)

    posts = await crud.post_list(session, request_params)
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(posts)}/{total}"
    return posts


@router.get("/{type}/{post_id}", response_model=SchemasReportPost, status_code=201)
async def get_post(
    post_id: int,
    type: str,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    # print(type)
    statistics = await crud.get_statistics(session, type, post_id)

    return statistics


@router.get(
    "/taboola", response_model=List[schemas_taboola.ReadTaboola], status_code=201
)
async def get_taboolas(
    response: Response,
    session: CurrentAsyncSession,
    request_params: TaboolaRequestParams,
    user: CurrentUser,
):
    filters = request_params.filters
    if filters.domain_id:
        # 网站下所有tab，1把所有网站下的文章查到，
        stmt = select(func.count(Taboola.id)).filter_by(
            **filters.dict(exclude_unset=True, exclude={"create"})
        )
        if filters.create:
            stmt = stmt.filter(cast(Taboola.create, DATE) == cast(filters.create, DATE))
    elif filters.post_id:
        # 在根据文章查到tab，统计
        stmt = select(func.count(distinct(ReportPost.taboola_id))).filter(
            ReportPost.post_id == filters.post_id
        )

    total = await session.scalar(stmt)
    taboolas = await crud.taboola_list(session=session, request_params=request_params)

    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(taboolas)} /{total}"
    return taboolas


@router.get("/browser", response_model=List[SchemasBrowser], status_code=201)
async def browser_list(
    response: Response,
    session: CurrentAsyncSession,
    request_params: BrowserRequestParams,
    user: CurrentUser,
) -> Any:
    total = await session.scalar(
        select(func.count(BrowserInfo.id)).filter(
            BrowserInfo.domain_id == request_params.record_id
        )
    )
    browsers = await crud.browser_list(session, request_params)

    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(browsers)} /{total}"
    return browsers


@router.get("/report", response_model=List[ReportSchema], status_code=201)
async def report_list(
    response: Response,
    session: CurrentAsyncSession,
    request_params: PostReportRequestParams,
) -> Any:
    total = await report_crud.total_report(session)
    reports = await report_crud.list_report(session, request_params)
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(reports)} /{total}"
    return reports


@router.get("/post/update_campaign/{item_id}", response_model=Msg)
async def post_update_campaign(
    item_id: str,
    user: CurrentUser,
    session: CurrentAsyncSession,
    active: bool = Query(...),
) -> Any:
    report: Optional[ReportPost] = await crud.get_taboola_by_item_id(session, item_id)
    if report is None:
        raise HTTPException(status_code=400, detail="找不到Id")
    apis = TaboolaApi()
    apis.get_token()
    status = apis.post_update_campaign(
        report.campaign_id, report.campaign_item_id, active
    )
    print(status)
    if ~status:
        raise HTTPException(status_code=400, detail=apis.msg)
    item_status: Optional[ItemStatus] = await session.scalar(
        select(ItemStatus).filter(
            ItemStatus.campaign_item_id == report.campaign_item_id
        )
    )
    if item_status is None:
        item_status = ItemStatus(
            campaign_item_id=report.campaign_item_id,
            post_id=report.post_id,
            status=active,
        )
        session.add(item_status)
    else:
        item_status.status = active
    await session.commit()

    return {"msg": apis.msg}


@router.get(
    "/taboola/update_campaign/{taboola_id}", response_model=Msg, status_code=201
)
async def taboola_update_campaign(
    taboola_id: int,
    user: CurrentUser,
    session: CurrentAsyncSession,
    active: bool = Query(...),
) -> Any:
    taboola: Optional[Taboola] = await crud.get_taboola_by_id(session, taboola_id)
    if taboola is None:
        return HTTPException(status_code=400, detail="taboola is not")
    apis = TaboolaApi()
    apis.get_token()
    operation = "ADD" if active else "REMOVE"
    if apis.taboola_update_campaign(taboola.site, operation):
        taboola.promotion = 0 if active else 1
        await session.commit()

    return {"msg": apis.msg}
