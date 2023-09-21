from sqlalchemy.orm import lazyload, joinedload
from typing import Optional
from sqlalchemy.orm import Session, selectinload
from app.models.report import VisitorIp, ReportPost, BrowserInfo, Post, Taboola
from app.models.domain import Domain
from app.schemas.report import Taboola as SchemasTaboola
from sqlalchemy import select, func
import re

from app.deps.request_params import ReportRequestParams


async def create_report(
    db: Session,
    visitor: Optional[VisitorIp],
    href: str,
    browser_id: int,
    post: Post,
    taboola: Optional[Taboola],
):
    is_page = True if href.find("page") != -1 else False
    report = ReportPost()
    report.post_id = post.id
    report.domain_id = post.domain_id
    report.is_page = is_page
    report.url = href
    report.browser_id = browser_id
    if taboola:
        report.taboola_id = taboola.id
    if visitor:
        report.visitor_ip = visitor.ip
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


async def get_taboola_by_site_id(db: Session, post:Optional[Post], site_id):
    _orm = select(Taboola).where(Taboola.site_id == site_id).options(joinedload(Taboola.posts.and_(Post.id==post.id)))
    taboola: Optional[Taboola | None] = (await db.execute(_orm)).scalar()
    return taboola


async def create_taboola(db: Session, post: Post,taboola_in=None):
    if taboola_in and taboola_in['site_id']:
        taboola: Optional[Taboola] = await get_taboola_by_site_id(db,post, taboola_in['site_id'])
        if taboola is None and isinstance(taboola_in, SchemasTaboola):
            taboola = Taboola(**taboola_in)
            taboola.posts.append(post)
            db.add(taboola)
            await db.commit()
        elif taboola:
            if len(taboola.posts) <= 0:
                taboola.posts.append(post)
                await db.commit()
            return taboola
    return None


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


async def create_browser(db: Session, user_agent, fingerprint_id, post: Post):
    if post is None:
        _orm = (
            select(BrowserInfo)
            .where(BrowserInfo.fingerprint_id == fingerprint_id)
            .options(joinedload(BrowserInfo.posts))
        )
    else:
        _orm = (
            select(BrowserInfo)
            .where(BrowserInfo.fingerprint_id == fingerprint_id)
            .options(joinedload(BrowserInfo.posts.and_(Post.id == post.id)))
        )
    browser: Optional[BrowserInfo | None] = (await db.execute(_orm)).scalar()
    # browser: Optional[BrowserInfo | None] = (await db.execute(_orm)).scalar()
    if browser is None:
        browser = BrowserInfo(fingerprint_id=fingerprint_id)
        browser.user_agent = user_agent
        browser.posts.append(post)
        db.add(browser)
        await db.commit()
        return browser
    if len(browser.posts) <= 0:
        browser.posts.append(post)
        await db.commit()
    return browser


async def create_visitor_ip(db: Session, client_host):
    # 判断是否有ip
    visitor = (
        await db.execute(select(VisitorIp).where(VisitorIp.ip == client_host))
    ).scalar()
    if visitor is None:
        visitor = VisitorIp(ip=client_host)  # 访客ip
        db.add(visitor)
        await db.commit()
    return visitor


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
