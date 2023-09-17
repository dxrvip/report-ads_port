from typing import Any, Optional, List, Dict
import re, urllib.parse
from fastapi import APIRouter, HTTPException, Header, Request, Response
from app.schemas.report import Report as ReportSchema
from app.schemas.report import Taboola as TaboolaSchema
from app.crud import report as crud
from app.schemas.msg import Msg
from app.schemas.report import ReportCreate
from app.models.report import Post, BrowserInfo, Taboola
from app.deps.users import CurrentAsyncSession, CurrentUser
from sqlalchemy.exc import IntegrityError

from app.crud.domain import get_domain_by_host
from app.deps.request_params import ReportRequestParams


router = APIRouter(prefix="/report")


@router.post("", response_model=Msg, status_code=201)
async def create_report(
    report_in: ReportCreate,
    session: CurrentAsyncSession,
    request: Request,
    href: Optional[str] = Header(None),
    slug: Optional[str] = Header(None),
    site_id: Optional[int] = Header(None),
    user_agent: Optional[str] = Header(None),
) -> Any:
    print(href, report_in, user_agent, site_id, "============")
  
    host = urllib.parse.urlparse(href).netloc
    domain = await get_domain_by_host(session, host)

    # 如果没有域名
    if domain is None or not slug or slug == "null" or slug == "undefined":
        raise HTTPException(402, detail="not post or domain")
    # 判断是否有taboola信息
    is_taboola = href.find("Taboola") > -1
    if is_taboola:
        # 插入taboola信息
        query: str = re.findall(r"\?(.+)$", href)[0]
        query_dict: Dict = {}
        for item in query.split("&"):
            [k, v] = item.split("=")
            query_dict[k] = int(v) if k == "site_id" or k == "campaign_id" else v
        taboola_in = TaboolaSchema(**query_dict)

    # 添加ip
    visitor_ip = await crud.create_visitor_ip(
        db=session, client_host=request.client.host
    )

    post: Optional[Post | None] = await crud.create_post(session, href, slug, domain)

    if is_taboola:
        taboola:Optional[Taboola] = await crud.create_taboola(session, taboola_in, post=post)
    else:
        taboola:Optional[Taboola] = await crud.get_taboola_by_click_id(session, None,site_id=site_id)
    
    # 浏览器指纹
    browser: BrowserInfo = await crud.create_browser(
        db=session,
        user_agent=user_agent,
        fingerprint_id=report_in.fingerprint_id,
        domain_id=domain.id,
        post=post
    )
    
    await crud.create_report(
        session, visitor_ip.id, href, browser.id, post, taboola
    )

    return {"msg": "success"}



@router.get("", response_model=List[ReportSchema], status_code=201)
async def get_reports(
    response: Response,
    session: CurrentAsyncSession,
    request_params: ReportRequestParams,
    user: CurrentUser,
) -> Any:
    total = await crud.total_report(session)
    reports = await crud.list_report(session, request_params)
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(reports)}/{total}"
    return reports


@router.get("/{report_id}", response_model=ReportSchema, status_code=201)
async def get_report(
    report_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    report: Optional[Post] = await crud.get_report(session, report_id)

    return report
