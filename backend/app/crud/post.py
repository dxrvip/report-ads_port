from sqlalchemy.orm import Session, joinedload
from typing import Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, distinct, cast, Integer
from typing import List, Optional
from app.models.report import Post, BrowserInfo, ReportPost, Taboola
from app.deps.request_params import (
    PostRequestParams,
    TaboolaRequestParams,
    BrowserRequestParams,
    PostReportRequestParams,
)


async def post_list(session: Session, request_params: PostRequestParams):
    _orm = (
        select(
            Post.url,
            Post.id,
            func.count(distinct(BrowserInfo.id)).label("bsum"),
            func.count(distinct(ReportPost.id)).label("rsum"),
            func.count(distinct(Taboola.id)).label("tsum"),
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


async def get_post_(db: Session, id):
    start_date = datetime.strptime("2023-09-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime("2023-09-21 23:59:59", "%Y-%m-%d %H:%M:%S")
    year = func.extract("year", ReportPost.create)
    month = func.extract("month", ReportPost.create)
    day = func.extract("day", ReportPost.create)
    _orm = (
        select(
            day.label("day"),
            year,
            month,
            func.sum(cast(ReportPost.is_page, Integer)).label("psum"),
            func.count(distinct(ReportPost.post_id)).label("rsum"),
            func.count(distinct(ReportPost.browser_id)).label("bsum"),
            func.count(distinct(ReportPost.taboola_id)).label("tsum"),
        )
        .filter(ReportPost.post_id == id)
        .where(ReportPost.create.between(start_date, end_date))

        .group_by(year, month, day)
    )
    # print(_orm)

    result = (await db.execute(_orm)).mappings()
    dict_row = [item for item in result]
    curret_date, row_dict = start_date, []
    psum, rsum, bsum, tsum = 0, 0, 0, 0
    while True:
        day = curret_date.day
        x: dict = {"id": day, "psum": 0, "rsum": 0, "bsum": 0, "tsum": 0}
        for index, row in enumerate(dict_row):
            if int(row.day) == day:
                x.update({**row})
                psum += row.psum
                rsum += row.rsum
                bsum += row.bsum
                tsum += row.tsum
                dict_row.pop(index)
                break
        x["date"] = curret_date.strftime("%Y-%m-%d")
        row_dict.append(x)
        curret_date = curret_date + timedelta(days=1)

        if curret_date >= end_date:
            break

    return {
        "result": row_dict,
        "id": 1,
        "total": {"翻页":  psum, "PV": rsum, "UV": bsum, "Taboola":tsum},
    }


async def taboola_list(session: Session, request_params: TaboolaRequestParams):
    _orm = (
        select(
            Taboola.id,
            Taboola.site_id,
            Taboola.platform,
            func.count(distinct(Post.id)).label("psum"),
            func.count(distinct(ReportPost.id)).label("rsum"),
            func.count(distinct(BrowserInfo.id)).label("bsum"),
        )
        .join(Taboola.posts, isouter=True)
        .join(ReportPost, isouter=True)
        .filter(Taboola.domain_id == request_params.record_id)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .group_by(Taboola.id)
        # .options(joinedload(Taboola.posts).subqueryload(Post.report_post))
    )
    print(_orm)
    # taboolas: Optional[List] = (await session.execute(_orm)).unique().all()
    taboolas: Optional[List] = (await session.execute(_orm)).all()
    if taboolas:
        taboolas = list(map(lambda x: x._asdict(), taboolas))

    return taboolas


async def browser_list(session: Session, request_params: BrowserRequestParams):
    _orm = (
        select(
            BrowserInfo.id,
            BrowserInfo.fingerprint_id,
            BrowserInfo.update_time,
            BrowserInfo.user_agent,
            func.count(distinct(Post.id)).label("psum"),
            func.count(distinct(ReportPost.id)).label("rsum"),
        )
        .filter(BrowserInfo.domain_id == request_params.record_id)
        .join(ReportPost, ReportPost.browser_id == BrowserInfo.id, isouter=True)
        .join(Post, ReportPost.post_id == Post.id)
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
