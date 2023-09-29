from fastapi import APIRouter, Query, HTTPException
from typing import List, Any, Optional
from app.schemas.msg import Msg
from sqlalchemy import distinct, select, func
from starlette.responses import Response
from app.schemas.post import (
    PostListReport as SchemasPost,
    ReportPost as SchemasReportPost,
)
from app.schemas.report import (
    ResultBrowserInfo as SchemasBrowser
)
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
from app.models.report import Post, Taboola, BrowserInfo, ReportPost
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
    total = await session.scalar(
        select(func.count(Post.id))
        .filter(Post.domain_id == request_params.domain_id)
    )
    
    
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
    if request_params.domain_id:
        # 网站下所有tab，1把所有网站下的文章查到，
        stmt = select(func.count(Taboola.id)).filter(
            Taboola.domain_id == request_params.domain_id
        )
    elif request_params.post_id:
        # 在根据文章查到tab，统计
        stmt = select(func.count(distinct(ReportPost.taboola_id))).filter(
            ReportPost.post_id == request_params.post_id
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


@router.get("/post/update_campaign/{post_id}", response_model=Msg, status_code=201)
async def post_update_campaign(
    post_id: int,user: CurrentUser,session: CurrentAsyncSession, active: bool = Query(...)
) -> Any:
    taboola: Optional[Taboola] = await crud.get_taboola_by_post_id(session, post_id)
    if taboola is None:
         return HTTPException(status_code=400, detail="taboola is not")
    apis = TaboolaApi()
    apis.get_token()
    if apis.post_update_campaign(taboola.campaign_id, taboola.campaign_item_id, active):
        post: Optional[Post] = await session.get(Post, post_id)
        post.promotion = 1 if active else 0
        await session.commit()

    return {"msg": apis.msg}


@router.get(
    "/taboola/update_campaign/{taboola_id}", response_model=Msg, status_code=201
)
async def taboola_update_campaign(
    taboola_id: int,user: CurrentUser,session: CurrentAsyncSession, active: bool = Query(...)
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
