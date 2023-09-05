from typing import Optional
from sqlalchemy.orm import Session, selectinload
from app.models.report import VisitorIp, ReportPost, BrowserInfo, Post, Taboola
from sqlalchemy import select, func
import re

from backend.app.deps.request_params import ReportRequestParams


async def create_report(
    db: Session, visitor_id: int, href: str, browser_id: int, post_id: int
):
    is_page = True if href.find("page") != -1 else False
    report = ReportPost(visitor_ip=visitor_id)
    report.post_id = post_id
    report.is_page = is_page
    report.url = href
    report.browser_id = browser_id
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


async def get_taboola_by_click_id(db: Session, click_id=None):
    if click_id is None:
        return None
    _orm = select(Taboola).where(Taboola.click_id == click_id)
    taboola: Optional[Taboola | None] = (await db.execute(_orm)).scalar()
    return taboola


async def create_taboola(db: Session, taboola_in, post):
    taboola = Taboola(**taboola_in.dict())
    taboola.posts.append(post)
    db.add(taboola)
    await db.commit()
    return taboola


async def create_post(
    db: Session, href: str, slug: str, taboola: Optional[Taboola | None]
):
    index = 1 if href.find("?") > -1 else 0
    url = re.search(r"^h(.+)\?|^(.+)$", href)[index]
    post: Post = Post(slug=slug, url=url)
    db.add(post)
    if taboola is not None:
        post.taboolas.append(taboola)
    await db.commit()
    return post


async def create_browser(db: Session, user_agent, fingerprint_id):
    browser = BrowserInfo(fingerprint_id=fingerprint_id)
    browser.user_agent = user_agent
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
    return (await db.execute(
        select(ReportPost)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .options(selectinload(ReportPost.post))
    )).scalars().all()
