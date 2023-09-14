from typing import Optional
from sqlalchemy.orm import Session, selectinload
from app.models.report import VisitorIp, ReportPost, BrowserInfo, Post, Taboola
from app.models.domain import Domain
from sqlalchemy import select, func
import re

from app.deps.request_params import ReportRequestParams


async def create_report(
    db: Session, visitor_id: int, href: str, browser_id: int, post: Post, taboola: Optional[Taboola]
):
    is_page = True if href.find("page") != -1 else False
    report = ReportPost(visitor_ip=visitor_id)
    report.post_id = post.id
    report.domain_id = post.domain_id
    report.is_page = is_page
    report.url = href
    report.browser_id = browser_id
    if taboola:
        report.taboola_id = taboola.id
    db.add(report)
    await db.commit()
    return report


async def get_post_by_slug(db: Session, slug: str):
    _orm = select(Post).where(Post.slug == slug)
    post: Optional[Post | None] = (await db.execute(_orm)).scalar()
    return post


async def get_browser(db: Session, fin_id: str):
    _orm = select(BrowserInfo).where(BrowserInfo.fingerprint_id == fin_id)
    browser: Optional[BrowserInfo | None] = (await db.execute(_orm)).scalar()
    return browser


async def get_taboola_by_click_id(db: Session, site_id=None):
    if site_id is None:
        return None
    _orm = select(Taboola).where(Taboola.site_id == site_id)
    taboola: Optional[Taboola | None] = (await db.execute(_orm)).scalar()
    return taboola


async def create_taboola(db: Session, taboola_in, post: Post):
    taboola = Taboola(**taboola_in.dict())
    taboola.domain_id = post.domain_id
    taboola.posts.append(post)
    db.add(taboola)
    await db.commit()
    return taboola


async def create_post(
    db: Session,
    href: str,
    slug: str,
    taboola: Optional[Taboola | None],
    domain: Optional[Domain],
):
    index = 1 if href.find("?") > -1 else 0
    url = re.search(r"^h(.+)\?|^(.+)$", href)[index]
    post: Post = Post(slug=slug, url=url)
    post.domain_id = domain.id
    db.add(post)
    if taboola is not None:
        post.taboolas.append(taboola)
    await db.commit()
    return post


async def create_browser(db: Session, user_agent, fingerprint_id, domain_id):
    browser = BrowserInfo(fingerprint_id=fingerprint_id)
    browser.user_agent = user_agent
    browser.domain_id = domain_id
    db.add(browser)
    await db.commit()
    return browser


async def create_visitor_ip(db: Session, client_host):
    visitor_ip = VisitorIp(ip=client_host)  # 访客ip
    db.add(visitor_ip)
    await db.commit()
    return visitor_ip


async def total_report(db: Session):
    report = await db.scalar(select(func.count(ReportPost.id)))
    return report


async def list_report(db: Session, request_params: ReportRequestParams):
    _orm = (
        select(ReportPost)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .options(selectinload(ReportPost.browser_info))
        .options(selectinload(ReportPost.visitor))
    )
    return (await db.execute(_orm)).scalars().all()


async def get_report(db:Session, report_id:int):
    
    _orm = (
        select(ReportPost)
        .where(ReportPost.id==report_id)
        .options(selectinload(ReportPost.browser_info))
        .options(selectinload(ReportPost.visitor))
        .options(selectinload(ReportPost.post))
        .options(selectinload(ReportPost.taboola_info))
    )

    report = (await db.scalar(_orm))
    return report