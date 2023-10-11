from typing import Any, Optional, Dict
from urllib.parse import urlparse, parse_qs
from fastapi import APIRouter, HTTPException, Header, Query
from app.schemas.report import Report as ReportSchema
from app.schemas.report import Taboola as TaboolaSchema
from app.crud import report as crud
from app.schemas.msg import Msg
from app.schemas.report import ReportCreate
from app.models.report import (
    ItemStatus,
    Post,
    BrowserInfo,
    Taboola,
    AdsClick,
    ReportPost,
)
from app.deps.users import CurrentAsyncSession, CurrentUser

from app.crud.domain import get_domain_by_host
from app.utils.ip_api import IpApi

# from app.deps.request_params import PostReportRequestParams


router = APIRouter(prefix="/report")


@router.put("/ads/{report_id}", response_model=Msg, status_code=201)
async def add_ads(
    db: CurrentAsyncSession,
    report_id: int,
    slug: Optional[str] = Header(None),
    site_id: Optional[str] = Header(None),
    fingerprint: Optional[str] = Header(None),
):
    print(slug, site_id, fingerprint, report_id)
    post, taboola, browser = None, None, None
    ads_click: AdsClick = AdsClick()
    if slug != "null":
        post: Optional[Post] = await crud.get_post_by_slug(db, slug)
    if site_id != "null":
        taboola: Optional[Taboola] = await crud.get_taboola_by_site_id(db, int(site_id))
    if fingerprint != "null":
        browser: Optional[BrowserInfo] = await crud.get_browser(db, fingerprint)
    if report_id:
        ads_click.report_id = report_id
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
    cf_connecting_ip: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
) -> Any:
    """
    1,site_id 进入带有 taboola追踪url
    2，无任何追踪代码
    3，带site_id翻页进入，或带site_id进入别的文章
    4, 如果是谷歌蜘蛛则不统计
    """
    print(f"{href}, {report_in}, {user_agent},============", cf_connecting_ip)
    if user_agent and user_agent.find("Googlebot") > 1:  # 如果是谷歌蜘蛛则不统计
        raise HTTPException(200, detail="googlebot")
    if len(user_agent) > 255:
        user_agent = user_agent[:255]
    is_taboola = href.find("site_id") > -1
    if not report_in.site_id and not is_taboola:
        raise HTTPException(200, detail="not site_id")
    o = urlparse(href)

    host = o.netloc
    domain = await get_domain_by_host(session, host)
    slug = o.path[1:] if len(o.path) > 0 else None
    # 如果没有域名  s
    if domain is None or slug is None:
        raise HTTPException(402, detail="not post or domain")
    # 判断是否有taboola信息

    if is_taboola:
        # 插入taboola信息
        q: Dict = parse_qs(o.query)
        query_dict: Dict = {k: v[0] for k, v in q.items()}
        taboola_in = TaboolaSchema(**query_dict)
        report_in = ReportCreate(**query_dict, fingerprint_id=report_in.fingerprint_id)

    # 添加ip
    if cf_connecting_ip:
        try:
            visitor_ip = await crud.create_visitor_ip(
                db=session, client_host=cf_connecting_ip
            )
        except:
            visitor_ip = await crud.get_database_ip(session, cf_connecting_ip)
    else:
        visitor_ip = None

    post: Optional[Post | None] = await crud.create_post(session, href, slug, domain)
    # 1, 不是taboola进入，2，带site——id进入，3，没有任何tab信息
    if is_taboola:  # 1, 不是taboola进入，2，带site——id进入
        taboola_in = taboola_in.dict()
    else:
        taboola_in = {"site_id": report_in.site_id}
    # https://www.pmsnhu.com/the-16-most-abandoned-places-around-the-world?click_id=GiDXjNWllJy6RBSAHpec-ZPjoMoWE-19obXB-BulL-i6hCCDk2Eo48y5jvrZ17LOAQ&tblci=GiDXjNWllJy6RBSAHpec-ZPjoMoWE-19obXB-BulL-i6hCCDk2Eo48y5jvrZ17LOAQ&campaign_id=27592800&campaign_item_id=3731635650&site_id=1143601&site=sliide-app1&platform=Smartphone#tblciGiDXjNWllJy6RBSAHpec-ZPjoMoWE-19obXB-BulL-i6hCCDk2Eo48y5jvrZ17LOAQ
    taboola: Optional[Taboola] = await crud.create_taboola(session, domain, taboola_in)
    # 浏览器指纹
    browser: Optional[BrowserInfo] = await crud.create_browser(
        db=session,
        user_agent=user_agent,
        fingerprint_id=report_in.fingerprint_id,
    )

    # 添加推广状态
    item_status: Optional[ItemStatus] = await crud.get_item_status_by_item_id(
        db=session, item_id=report_in.campaign_item_id
    )

    if item_status is None:
        item_status = ItemStatus(
            campaign_item_id=report_in.campaign_item_id,
            post_id=post.id,
            status=True,
        )
        session.add(item_status)
        await session.commit()
    else:
        item_status.status = True
        await session.commit()
    report = await crud.create_report(
        session, visitor_ip, href, browser, post, taboola, report_in
    )
    try:
        show = True
        check_ip = IpApi(ip_address=visitor_ip.ip)
        check_ip.get_ip()
        if check_ip.status == "success":
            visitor_ip.hosting = check_ip.hosting
            visitor_ip.proxy = check_ip.proxy
            await session.commit()
        if check_ip.hosting or check_ip.proxy:
            show = False
        return {"msg": "success", "id": report.id, "show": show}
    except:
        pass
    return {"msg": "success", "id": report.id, "show": True}


@router.get("/{report_id}", response_model=ReportSchema, status_code=201)
async def get_report(
    report_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    report: Optional[Post] = await crud.get_report(session, report_id)

    return report


@router.put("/{report_id}", response_model=Msg, status_code=201)
async def put_report(
    report_id: int, session: CurrentAsyncSession, ads_sum: Optional[int] = Query(...)
) -> Any:
    if ads_sum and ads_sum > 0:
        report: Optional[ReportPost] = await session.get(ReportPost, report_id)
        if report is not None:
            report.ads_show_sum = ads_sum
            await session.commit()
        return {"msg": "ok"}
    return {"msg": ""}
