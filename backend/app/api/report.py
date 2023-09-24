from typing import Any, Optional, List, Dict,Union
import re, urllib.parse
from fastapi import APIRouter, HTTPException, Header, Request, Response
from app.schemas.report import Report as ReportSchema
from app.schemas.report import Taboola as TaboolaSchema
from app.crud import report as crud
from app.schemas.msg import Msg
from app.schemas.report import ReportCreate
from app.models.report import Post, BrowserInfo, Taboola, AdsClick
from app.deps.users import CurrentAsyncSession, CurrentUser
from sqlalchemy.exc import IntegrityError

from app.crud.domain import get_domain_by_host
# from app.deps.request_params import PostReportRequestParams


router = APIRouter(prefix="/report")


@router.put("/ads", response_model=Msg, status_code=201)
async def add_ads(
    db: CurrentAsyncSession,
    slug: Optional[str] = Header(None),
    site_id: Optional[str] = Header(None),
    fingerprint: Optional[str] = Header(None),
):
    print(slug, site_id, fingerprint)
    post, taboola, browser = None,None,None
    if slug != 'null':
        post: Optional[Post] = await crud.get_post_by_slug(db, slug)
    if site_id != 'null':
        taboola: Optional[Taboola] = await crud.get_taboola_by_site_id(db, int(site_id))
    if fingerprint != 'null':
        browser: Optional[BrowserInfo] = await crud.get_browser(db, fingerprint)
    ads_click: AdsClick = AdsClick()
    if not browser and not post and not taboola:
        return {"msg": "error"}
    if browser:
        ads_click.browser_id = browser.id
    if post:
        ads_click.post_id = post.id
    if taboola:
        ads_click.taboola_id = taboola.id
    db.add(ads_click)
    await db.commit()
    return {"msg": ""}


@router.post("", response_model=Msg, status_code=201)
async def create_report(
    report_in: ReportCreate,
    session: CurrentAsyncSession,
    href: Optional[str] = Header(None),
    slug: Optional[str] = Header(None),
    site_id: Optional[int | str] = Header(None),
    ip: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
) -> Any:
    
    print(f"{href}, {report_in}, {user_agent},  {ip}, {site_id},============")
    if len(user_agent) > 255:
        user_agent = user_agent[:255]
    is_taboola = href.find("site_id") > -1
    if site_id == 'null' and not is_taboola:
        raise HTTPException(200, detail="not site_id")
    host = urllib.parse.urlparse(href).netloc
    domain = await get_domain_by_host(session, host)

    # 如果没有域名  s
    if domain is None or not slug or slug == "null" or slug == "undefined":
        raise HTTPException(402, detail="not post or domain")
    # 判断是否有taboola信息
    
    if is_taboola:
        # 插入taboola信息
        query: str = re.findall(r"\?(.+)$", href)[0]
        query_dict: Dict = {}
        for item in query.split("&"):
            [k, v] = item.split("=")
            query_dict[k] = int(v) if k == "site_id" or k == "campaign_id" else v
        taboola_in = TaboolaSchema(**query_dict)

    # 添加ip
    if ip and ip != 'null':
        visitor_ip = await crud.create_visitor_ip(
            db=session, client_host=ip
        )
    else:
        visitor_ip = None

    post: Optional[Post | None] = await crud.create_post(session, href, slug, domain)
    # 1, 不是taboola进入，2，带site——id进入，3，没有任何tab信息
    if is_taboola: # 1, 不是taboola进入，2，带site——id进入
        taboola_in = taboola_in.dict()
    else:
        taboola_in = {"site_id":site_id}
   #https://www.pmsnhu.com/the-16-most-abandoned-places-around-the-world?click_id=GiDXjNWllJy6RBSAHpec-ZPjoMoWE-19obXB-BulL-i6hCCDk2Eo48y5jvrZ17LOAQ&tblci=GiDXjNWllJy6RBSAHpec-ZPjoMoWE-19obXB-BulL-i6hCCDk2Eo48y5jvrZ17LOAQ&campaign_id=27592800&campaign_item_id=3731635650&site_id=1143601&site=sliide-app1&platform=Smartphone#tblciGiDXjNWllJy6RBSAHpec-ZPjoMoWE-19obXB-BulL-i6hCCDk2Eo48y5jvrZ17LOAQ
    taboola: Optional[Taboola] = await crud.create_taboola(
    session, domain, taboola_in
    ) 
    # 浏览器指纹
    browser: Optional[BrowserInfo] = await crud.create_browser(
        db=session,
        user_agent=user_agent,
        fingerprint_id=report_in.fingerprint_id,
    )

    await crud.create_report(session, visitor_ip, href, browser, post, taboola)

    return {"msg": "success"}


# @router.get("", response_model=List[ReportSchema], status_code=201)
# async def get_reports(
#     response: Response,
#     session: CurrentAsyncSession,
#     request_params: PostReportRequestParams,
#     user: CurrentUser,
# ) -> Any:
#     total = await crud.total_report(session)
#     reports = await crud.list_report(session, request_params)
#     response.headers[
#         "Content-Range"
#     ] = f"{request_params.skip}-{request_params.skip + len(reports)}/{total}"
#     return reports


@router.get("/{report_id}", response_model=ReportSchema, status_code=201)
async def get_report(
    report_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    report: Optional[Post] = await crud.get_report(session, report_id)

    return report

