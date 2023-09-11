from sqlalchemy.orm import Session, joinedload
from typing import Any
from sqlalchemy import select, func, distinct, text
from typing import List, Optional
from app.models.report import Post, BrowserInfo, ReportPost, Taboola
from app.deps.request_params import PostRequestParams, TaboolaRequestParams, BrowserRequestParams, PostReportRequestParams


async def post_list(session: Session, request_params: PostRequestParams):
    _orm = (
        select(
            Post.url,
            Post.id,
            func.count(distinct(BrowserInfo.id)).label("bsum"),
            func.count(distinct(ReportPost.id)).label("rsum"),
            func.count(distinct(text("post_taboola_table_1.id"))).label("tsum"),
        )
        .filter(Post.domain_id == request_params.record_id)
        .join(ReportPost, Post.id == ReportPost.post_id, isouter=True)
        .join(BrowserInfo, Post.id == BrowserInfo.post_id, isouter=True)
        .join(Post.taboolas, isouter=True)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .group_by(Post.id)
    )
    print(_orm)
    posts: Optional[List] = (await session.execute(_orm)).all()
    if posts:
        posts = list(map(lambda x: x._asdict(), posts))
    return posts


async def taboola_list(session: Session, request_params: TaboolaRequestParams):
    _orm = (
        select(Taboola)
        .filter(Post.domain_id == request_params.record_id)
        .join(Taboola.posts)
        .join(ReportPost)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .options(joinedload(Taboola.posts).subqueryload(Post.report_post))
        .add_columns(Taboola.id)
    )
    print(_orm)
    taboolas: Optional[List] = (await session.execute(_orm)).unique().all()
    repola = []
    if taboolas:
        for item in taboolas:
            r = {"id": item.id}
            
            r['psum'] = len(item.Taboola.posts)
            rsum = 0
            for i in item.Taboola.posts:
                rsum =rsum + len(i.report_post)
            r['rsum'] = rsum
            r['site_id'] = item.Taboola.site_id
            r['platform'] = item.Taboola.platform
            repola.append(r)
            
    if taboolas:
        taboolas = list(map(lambda x: x._asdict(), taboolas))

    return repola

async def browser_list(session: Session, request_params: BrowserRequestParams):

    _orm = (
        select(BrowserInfo.id, BrowserInfo.fingerprint_id, BrowserInfo.update_time, BrowserInfo.user_agent,
               func.count(distinct(Post.id)).label("psum"),
               func.count(distinct(ReportPost.id)).label("rsum"))
        .filter(BrowserInfo.domain_id == request_params.record_id)
        .join(ReportPost, ReportPost.browser_id==BrowserInfo.id, isouter=True)
        .join(Post, ReportPost.post_id==Post.id)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .group_by(BrowserInfo.id)
    )
    print(_orm)
    browsers: Optional[List] = (await session.execute(_orm)).all()
    if browsers:
        browsers = list(map(lambda x: x._asdict(), browsers))
    return browsers

async def reports_list(session: Session, request_params: PostReportRequestParams):

    _orm = (
        select(ReportPost, ReportPost.id, ReportPost.url, ReportPost.create)
        .filter(ReportPost.domain_id == request_params.record_id)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
    )

    reports: Optional[List] = (await session.execute(_orm)).all()
    if reports:
        reports = list(map(lambda x: x._asdict(), reports))
    return reports