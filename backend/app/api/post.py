from fastapi import APIRouter, HTTPException
from typing import List, Any, Optional
from sqlalchemy import select, func
from starlette.responses import Response
from app.schemas.post import PostListReport as SchemasPost, ReportPost as SchemasReportPost
from app.schemas.report import ResultTaboola as SchemasTaboola, ResultBrowserInfo as SchemasBrowser, ResultReport as SchemasReport
from app.deps.users import CurrentUser
from app.deps.db import CurrentAsyncSession
from app.deps.request_params import PostRequestParams, TaboolaRequestParams,BrowserRequestParams, PostReportRequestParams
from app.crud import post as crud
from app.models.report import Post, Taboola, BrowserInfo, ReportPost


router = APIRouter(prefix="/list")

# 
@router.get("/post", response_model=List[SchemasPost], status_code=201)
async def get_posts(
    response: Response,
    session: CurrentAsyncSession,
    request_params: PostRequestParams,
    user: CurrentUser,
) -> Any:
    total = await session.scalar(select(func.count(Post.id)).filter(Post.domain_id==request_params.record_id))
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
    statistics= await crud.get_statistics(session,type , post_id)

    return statistics



@router.get("/taboola", response_model=List[SchemasTaboola], status_code=201)
async def get_taboolas(
    response: Response,
    session: CurrentAsyncSession,
    request_params: TaboolaRequestParams,
    user: CurrentUser 
):
    total = await session.scalar(select(func.count(Taboola.id)))
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
    user: CurrentUser
    )-> Any:
    
    total = await session.scalar(select(func.count(BrowserInfo.id)).filter(BrowserInfo.domain_id==request_params.record_id))
    browsers = await crud.browser_list(session, request_params)


    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(browsers)} /{total}"
    return browsers

@router.get("/report", response_model=List[SchemasReport], status_code=201)
async def report_list(
    response: Response,
    session: CurrentAsyncSession,
    request_params: PostReportRequestParams,
    user: CurrentUser
    )-> Any:
    
    total = await session.scalar(select(func.count(ReportPost.id)).filter(ReportPost.domain_id==request_params.record_id))
    reports = await crud.reports_list(session, request_params)
    response.headers[
        "Content-Range"
    
    ] = f"{request_params.skip}-{request_params.skip + len(reports)} /{total}"
    return reports

