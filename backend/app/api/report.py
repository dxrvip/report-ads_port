from typing import Any, Optional, List, Dict
import re, urllib.parse
from fastapi import APIRouter, HTTPException, Header, Request, Response
from app.schemas.report import Report as ReportSchema
from app.schemas.report import Taboola as TaboolaSchema
from app.crud import report as crud
from app.schemas.msg import Msg
from app.schemas.report import ReportCreate
from app.models.report import Post, BrowserInfo
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
    user_agent: Optional[str] = Header(None),
) -> Any:
    print(href, report_in.dict(), user_agent)
    try:
        host = urllib.parse.urlparse(href).netloc
        domain = await get_domain_by_host(session, host)

        # 如果没有域名
        if domain is None:
            raise HTTPException(404, detail="无聊的请求")
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

        # 浏览器指纹
        browser: Optional[BrowserInfo | None] = await crud.get_browser(
            db=session, fin_id=report_in.fingerprint_id
        )
        if browser is None:
            # 添加浏览器指纹信息
            browser = await crud.create_browser(
                db=session,
                user_agent=user_agent,
                fingerprint_id=report_in.fingerprint_id,
                domain_id=domain.id
            )
        # 该访问请求是否是帖子
        if not slug or slug == "null" or slug == "undefined":
            return {"msg": "ok No1"}
        post: Optional[Post | None] = await crud.get_post_by_slug(db=session, slug=slug)
        # 判断帖子是否插入表
        if post is None:
            click_id = query_dict.get("click_id") if is_taboola else None
            taboola = await crud.get_taboola_by_click_id(
                session, click_id
            )
            # 插入帖子
            post = await crud.create_post(session, href, slug, taboola, domain)
            if taboola is None and is_taboola:
                taboola = await crud.create_taboola(session, taboola_in, post=post)
        else:
            # 添加taboola
            if is_taboola:
                taboola = await crud.create_taboola(session, taboola_in, post=post)
        taboola = taboola if is_taboola else None
        await crud.create_report(
            session, visitor_ip.id, href, browser.id, post, taboola
        )
        
        return {"msg": "success"}

    except IntegrityError:
        raise HTTPException(402, detail="error")

    except Exception as err:
        print(err)
        raise HTTPException(402, detail="error")


@router.get("", response_model=List[ReportSchema], status_code=201)
async def get_reports(
    response: Response,
    session: CurrentAsyncSession,
    request_params: ReportRequestParams,
    user: CurrentUser
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

