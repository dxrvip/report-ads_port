from sqlalchemy.orm import (
    Session,
    joinedload,
    defaultload,
    selectinload,
    subqueryload,
    aliased,
)
from typing import Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, distinct, cast, case, Integer, text
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
            Post.create_time,
            Post.promotion,
            # func.sum(cast(ReportPost.is_page, Integer)).label("page_sum"),
            func.count(distinct(ReportPost.id)).label("rsum"),
            func.count(distinct(ReportPost.taboola_id)).label("tsum"),
            func.count(distinct(ReportPost.browser_id)).label("bsum"),
        )
        .filter(Post.domain_id == request_params.record_id)
        .join(ReportPost, Post.id == ReportPost.post_id)
        # .outerjoin(Post.taboolas)
        # .outerjoin(Post.browser_info)
        .options(selectinload(Post.browser_info).selectinload(BrowserInfo.posts))
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(
            request_params.order_by
        )  # 一项重要的技术（特别是在某些数据库后端上）是能够对 columns 子句中已声明的表达式进行 ORDER BY 或 GROUP BY，而无需在 ORDER BY 或 GROUP BY 子句中重新声明表达式，而是使用列COLUMNS 子句中的名称或标记名称。通过将名称的字符串文本传递给 Select.order_by()orSelect.group_by()方法可以使用此形式。传递的文本并不直接渲染；相反，为 columns 子句中的表达式指定的名称，并在上下文中呈现为该表达式名称，如果未找到匹配项，则会引发错误。一元修饰符 asc()anddesc()也可以这种形式使用：
        .group_by(Post.id)
        .add_columns(Post)
    )
    # print(_orm)
    posts: Optional[List] = (await session.execute(_orm)).unique().all()
    posts_dict = []
    for item in posts:
        # print(item)
        zssum = 0
        for browser in item.Post.browser_info:
            if len(browser.posts) > 1:
                zssum += 1
        item = item._asdict()
        item["zssum"] = zssum
        posts_dict.append(item)
    # if posts:
    #     posts = list(map(lambda x: x._asdict(), posts))
    return posts_dict


async def get_statistics(db: Session, type, id):
    """
    统计数据
    """
    day = func.extract("day", ReportPost.create)

    if type == "post":
        t = ReportPost.post_id == id
    elif type == "taboola":
        t = ReportPost.taboola_id == id
    elif type == "browser":
        t = ReportPost.browser_id == id
    end_date = datetime.now()
    start_date = datetime.now() - timedelta(days=7)
    _orm = (
        select(
            day.label("day"),
            func.sum(cast(ReportPost.is_page, Integer)).label("psum"),
            func.count(distinct(ReportPost.id)).label("rsum"),
            func.count(distinct(ReportPost.browser_id)).label("bsum"),
            func.count(distinct(ReportPost.browser_id)).label("zssum"),
            func.count(distinct(ReportPost.taboola_id)).label("tsum"),
        )
        .select_from(Post)
        .join(ReportPost, ReportPost.post_id == Post.id)
        .where(ReportPost.create.between(start_date, end_date), t)
        .group_by(
            func.extract("year", ReportPost.create),
            func.extract("month", ReportPost.create),
            day,
        )
    )
    print(_orm)
    result = (await db.execute(_orm)).mappings()
    dict_row = [item for item in result]
    curret_date, row_dict = start_date, []
    psum, rsum, bsum, tsum, zssum = 0, 0, 0, 0, 0
    while True:
        day = curret_date.day
        x: dict = {"id": day, "psum": 0, "rsum": 0, "bsum": 0, "tsum": 0, "zssum": 0}
        for index, row in enumerate(dict_row):
            if int(row.day) == day:
                x.update({**row})
                psum += row.psum
                rsum += row.rsum
                bsum += row.bsum
                tsum += row.tsum
                zssum += row.zssum
                dict_row.pop(index)
                break
        x["date"] = curret_date.strftime("%Y-%m-%d")
        row_dict.append(x)

        if curret_date >= end_date:
            break
        curret_date = curret_date + timedelta(days=1)
    return {
        "result": row_dict,
        "id": 1,
    }


async def taboola_list(session: Session, request_params: TaboolaRequestParams):
    subquery = (
        select(Taboola.id)
        .join(Post.taboolas)
        .where(Post.id == request_params.record_id, Post.domain_id == 2)
        .subquery()
    )
    taboola_ali = aliased(Taboola, subquery)
    post2 = aliased(Post)
    post1 = aliased(Post)
    _orm = (
        select(
            Taboola.id,
            Taboola.site_id,
            Taboola.create,
            Taboola.promotion,
            func.count(distinct(post1.id)).label("post_sum"),
            func.count(distinct(ReportPost.id)).label("report_sum"),
            func.count(distinct(ReportPost.browser_id)).label("ip_sum"),
            (
                func.sum(cast(ReportPost.is_page, Integer))
                / func.count(distinct(post1.id))
            ).label("page_sum"),
            (
                func.count(distinct(ReportPost.browser_id))
                - func.count(distinct(post2.id))
            ).label("zs_sum"),
        )
        .select_from(Taboola)
        .join(taboola_ali, Taboola.id == taboola_ali.id)
        .join(Taboola.posts.of_type(post1))
        .join(ReportPost, ReportPost.taboola_id == Taboola.id)
        .join(BrowserInfo, BrowserInfo.id == ReportPost.browser_id)
        # .add_columns(BrowserInfo)
        .join(BrowserInfo.posts.of_type(post2))
        .group_by(Taboola.id)
    )
    print(_orm)

    # _orm = (
    #     select(
    #         Taboola.id,
    #         Taboola.site_id,
    #         Taboola.create,
    #         Taboola.promotion,
    #         func.sum(cast(ReportPost.is_page, Integer)).label("page_sum"),
    #         func.count(distinct(ReportPost.post_id)).label("post_sum"),
    #         func.count(distinct(ReportPost.id)).label("report_sum"),
    #         func.count(distinct(ReportPost.visitor_ip)).label("ip_sum"),
    #     )
    #     .join(Taboola.posts)
    #     .join(ReportPost, ReportPost.post_id == Post.id, isouter=True)
    #     .where(
    #         Taboola.id.in_(select(Taboola.id).join(Taboola.posts.and_(Post.id == request_params.record_id))),
    #         ReportPost.taboola_id==Taboola.id
    #     )
    #     .offset(request_params.skip)
    #     .limit(request_params.limit)
    #     .order_by(request_params.order_by)
    #     .group_by(Taboola.id)
    # )
    taboolas: Optional[List] = (await session.execute(_orm)).all()
    # if taboolas:
    #    https://www.pmsnhu.com/these-15-travel-destinations-are-worth-the-hype-versus-those-that-dont?click_id=GiDNq7JpdZ_3kYVmk-jWgGLJBIPYS7z_zTobYgppyu2wqCCDk2EorZLR77DegcEm&tblci=GiDNq7JpdZ_3kYVmk-jWgGLJBIPYS7z_zTobYgppyu2wqCCDk2EorZLR77DegcEm&
    # campaign_id=27592800
    # &campaign_item_id=3731635642
    # &site_id=1536824
    # &site=laptopsvilla-publisher
    # &utm_source=Taboola
    # &platform=Smartphone#tblciGiDNq7JpdZ_3kYVmk-jWgGLJBIPYS7z_zTobYgppyu2wqCCDk2EorZLR77DegcEm

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
        # .filter(BrowserInfo.domain_id == request_params.record_id)
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


async def get_post_by_post_id(session: Session, post_id) -> Any:
    _orm = (
        select(Taboola)
        .join(Taboola.posts.and_(Post.id == post_id))
        .options(joinedload(Taboola.posts.and_(Post.id == post_id)))
    )
    taboola: Optional[Taboola] = (await session.execute(_orm)).scalar()
    return taboola


async def get_taboola_by_post_id(session: Session, taboola_id) -> Any:
    _orm = select(Taboola).where(Taboola.id == taboola_id)
    taboola: Optional[Taboola] = (await session.execute(_orm)).scalar()
    return taboola
