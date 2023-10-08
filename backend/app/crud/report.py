from sqlalchemy.orm import lazyload, joinedload
from typing import Optional
from sqlalchemy.orm import Session, selectinload, subqueryload
from app.models.report import (
    ItemStatus,
    VisitorIp,
    ReportPost,
    BrowserInfo,
    Post,
    Taboola,
)
from app.models.domain import Domain
from app.schemas.report import ReportCreate, Taboola as SchemasTaboola
from sqlalchemy import select, func
import re

from app.deps.request_params import PostReportRequestParams


async def create_report(
    db: Session,
    visitor: Optional[VisitorIp],
    href: str,
    browser: Optional[BrowserInfo],
    post: Post,
    taboola: Optional[Taboola],
    report_in: ReportCreate,
):
    is_page = True if href.find("page") != -1 else False
    report = ReportPost()
    report.post_id = post.id
    report.domain_id = post.domain_id
    report.is_page = is_page
    report.url = href
    report.campaign_id = report_in.campaign_id
    report.campaign_item_id = report_in.campaign_item_id
    if browser:
        report.browser_id = browser.id
    if taboola:
        report.taboola_id = taboola.id
    if visitor:
        report.visitor_ip = visitor.id
    db.add(report)
    await db.commit()
    return report


async def get_post_by_slug(db: Session, slug: str):
    _orm = select(Post).where(Post.slug == slug)
    post: Optional[Post | None] = (await db.scalars(_orm)).first()
    return post


async def get_browser(db: Session, fin_id: str):
    _orm = select(BrowserInfo).where(BrowserInfo.fingerprint_id == fin_id)
    browser: Optional[BrowserInfo | None] = (await db.execute(_orm)).scalar()
    return browser


async def get_taboola_by_site_id(db: Session, site_id):
    _orm = select(Taboola).where(Taboola.site_id == site_id)
    taboola: Optional[Taboola | None] = (await db.execute(_orm)).scalar()
    return taboola


async def create_taboola(db: Session, domain: Domain, taboola_in=None):
    taboola: Optional[Taboola] = await get_taboola_by_site_id(db, taboola_in["site_id"])
    if taboola is None and len(taboola_in) > 1:
        taboola = Taboola(**taboola_in)
        taboola.domain_id = domain.id
        db.add(taboola)
        await db.commit()
    return taboola


async def create_post(
    db: Session,
    href: str,
    slug: str,
    domain: Optional[Domain],
):
    post: Optional[Post | None] = await get_post_by_slug(db=db, slug=slug)
    if post is None:
        index = 1 if href.find("?") > -1 else 0
        url = re.search(r"^(.+)\?|^(.+)$", href)[index]
        post: Post = Post(slug=slug, url=url)
        post.domain_id = domain.id
        db.add(post)
        await db.commit()
    return post


async def create_browser(db: Session, user_agent, fingerprint_id):
    _orm = select(BrowserInfo).filter(BrowserInfo.fingerprint_id == fingerprint_id)

    browser: Optional[BrowserInfo | None] = (await db.execute(_orm)).scalar()
    if browser is None:
        browser = BrowserInfo(fingerprint_id=fingerprint_id)
        browser.user_agent = user_agent
        db.add(browser)
        await db.commit()
    return browser


async def get_database_ip(db, client_host):
    ip: Optional[VisitorIp] = (
        await db.execute(select(VisitorIp).where(VisitorIp.ip == client_host))
    ).scalar()
    return ip


async def create_visitor_ip(db: Session, client_host):
    # 判断是否有ip
    visitor = await get_database_ip(db, client_host)
    if visitor is None:
        visitor = VisitorIp(ip=client_host)  # 访客ip
        db.add(visitor)
        await db.commit()
    return visitor


async def total_report(db: Session):
    report = await db.scalar(select(func.count(ReportPost.id)))
    return report


async def get_item_status_by_item_id(db: Session, item_id: str) -> ItemStatus:
    item_status: Optional[ItemStatus] = await db.scalar(
        select(ItemStatus).filter(ItemStatus.campaign_item_id == item_id)
    )
    return item_status


async def list_report(db: Session, request_params: PostReportRequestParams):
    _orm = (
        select(ReportPost)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .options(selectinload(ReportPost.browser_info))
        .options(selectinload(ReportPost.visitor))
        .options(subqueryload(ReportPost.taboola_info))
    )
    return (await db.execute(_orm)).scalars().all()


async def get_report(db: Session, report_id: int):
    _orm = (
        select(ReportPost)
        .where(ReportPost.id == report_id)
        .options(selectinload(ReportPost.browser_info))
        .options(selectinload(ReportPost.visitor))
        .options(selectinload(ReportPost.post))
        .options(selectinload(ReportPost.taboola_info))
    )

    report = await db.scalar(_orm)
    return report
