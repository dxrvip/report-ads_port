from sqlalchemy.orm import (
    Session,
    joinedload,
    # defaultload,
    # selectinload,
    # subqueryload,
    # aliased,
)
from typing import Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, distinct, cast, Integer, case
from typing import List, Optional
from app.models.report import Post, BrowserInfo, ReportPost, Taboola, AdsClick
from app.deps.request_params import (
    PostRequestParams,
    TaboolaRequestParams,
    BrowserRequestParams,
    PostReportRequestParams,
)


subquery = (
    select(
        BrowserInfo.id,
        case((func.count(distinct(ReportPost.post_id)) > 1, 1), else_=0).label(
            "zs_count"
        ),
    )
    .join(ReportPost, ReportPost.browser_id == BrowserInfo.id)
    .group_by(BrowserInfo.id)
    .subquery()
)


def ads_tablie_subquery(start_date=None, end_date=None):
    if start_date and end_date:
        return (
            select(ReportPost.id, func.count(AdsClick.id))
            .outerjoin(AdsClick, AdsClick.post_id == ReportPost.post_id)
            .where(AdsClick.create.between(start_date, end_date))
            .group_by(ReportPost.id)
            .subquery()
        )
    else:
        return (
            select(ReportPost.id, func.count(AdsClick.id))
            .outerjoin(AdsClick, AdsClick.post_id == ReportPost.post_id)
            .group_by(ReportPost.id)
            .subquery()
        )


async def post_list(session: Session, request_params: PostRequestParams):
    ads_click_subquey = ads_tablie_subquery()
    stmt = (
        select(
            Post.url,
            Post.id,
            Post.create_time,
            Post.promotion,
            func.sum(cast(ReportPost.is_page, Integer)).label("page_sum"),
            func.count(distinct(ReportPost.id)).label("report_count"),
            func.count(distinct(ReportPost.taboola_id)).label("taboola_count"),
            func.count(distinct(ReportPost.browser_id)).label("borwser_count"),
            func.count(distinct(ReportPost.visitor_ip)).label("ip_count"),
            func.sum(subquery.c.zs_count).label("zs_sum"),
            func.sum(case((ReportPost.url.like("%site%"), 1), else_=0)).label(
                "tab_open_sum"
            ),
            (func.sum(ads_click_subquey.c.count) / func.count(ReportPost.id)).label(
                "ads_count"
            ),
        )
        .filter(Post.domain_id == request_params.domain_id)
        .join(ReportPost, Post.id == ReportPost.post_id)
        .join(subquery, ReportPost.browser_id == subquery.c.id)
        .join(ads_click_subquey, ads_click_subquey.c.id == ReportPost.id)
        # .options(selectinload(Post.browser_info).selectinload(BrowserInfo.posts))
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(
            request_params.order_by
        )  # 一项重要的技术（特别是在某些数据库后端上）是能够对 columns 子句中已声明的表达式进行 ORDER BY 或 GROUP BY，而无需在 ORDER BY 或 GROUP BY 子句中重新声明表达式，而是使用列COLUMNS 子句中的名称或标记名称。通过将名称的字符串文本传递给 Select.order_by()orSelect.group_by()方法可以使用此形式。传递的文本并不直接渲染；相反，为 columns 子句中的表达式指定的名称，并在上下文中呈现为该表达式名称，如果未找到匹配项，则会引发错误。一元修饰符 asc()anddesc()也可以这种形式使用：
        .group_by(Post.id)
        # .add_columns(ReportPost)
    )
    posts: Optional[List] = (await session.execute(stmt)).all()
    return posts


async def post_statistics(
    db: Session, id: int, start_date: datetime, end_date: datetime
):
    """文章单独统计数据"""
    day = func.extract("day", ReportPost.create)
    ads_click_subquery = ads_tablie_subquery()
    stmt = (
        select(
            day.label("day"),
            func.sum(cast(ReportPost.is_page, Integer)).label("page_sum"),
            func.count(distinct(ReportPost.id)).label("report_count"),
            func.count(distinct(ReportPost.taboola_id)).label("taboola_count"),
            func.count(distinct(ReportPost.browser_id)).label("borwser_count"),
            func.count(distinct(ReportPost.visitor_ip)).label("ip_count"),
            func.sum(subquery.c.zs_count).label("zs_sum"),
            func.sum(case((ReportPost.url.like("%site%"), 1), else_=0)).label(
                "tab_open_sum"
            ),
            (func.sum(ads_click_subquery.c.count) / func.count(ReportPost.id)).label(
                "ads_count"
            ),
        )
        .select_from(Post)
        .join(ReportPost, ReportPost.post_id == Post.id)
        .join(subquery, ReportPost.browser_id == subquery.c.id)
        .join(ads_click_subquery, ads_click_subquery.c.id == ReportPost.id)
        .where(ReportPost.create.between(start_date, end_date), Post.id == id)
        .group_by(
            func.extract("year", ReportPost.create),
            func.extract("month", ReportPost.create),
            day,
        )
    )
    result = (await db.execute(stmt)).mappings()
    dict_row = [item for item in result]
    curret_date, row_dict = start_date, []
    while True:
        day = curret_date.day
        x: dict = {
            "id": day,
            "page_sum": 0,
            "report_count": 0,
            "borwser_count": 0,
            "taboola_count": 0,
            "zs_sum": 0,
            "ip_count": 0,
            "tab_open_sum": 0,
            "ads_count": 0,
        }
        for index, row in enumerate(dict_row):
            if int(row.day) == day:
                x.update({**row})
                dict_row.pop(index)
                break
        x["date"] = curret_date.strftime("%Y-%m-%d")
        row_dict.append(x)

        if curret_date >= end_date:
            break
        curret_date = curret_date + timedelta(days=1)
    return row_dict


async def post_date_total(db, id, start_date, end_date):
    ads_click_subquery = ads_tablie_subquery()
    stmt = (
        select(
            ReportPost.post_id,
            func.sum(cast(ReportPost.is_page, Integer)).label("page_sum"),
            func.count(distinct(ReportPost.taboola_id)).label("taboola_count"),
            func.count(distinct(ReportPost.browser_id)).label("browser_count"),
            func.count(distinct(ReportPost.visitor_ip)).label("ip_count"),
            func.count(distinct(ReportPost.id)).label("report_count"),
            func.sum(subquery.c.zs_count).label("zs_sum"),
            func.sum(case((ReportPost.url.like("%site%"), 1), else_=0)).label(
                "tab_open_sum"
            ),
            (func.sum(ads_click_subquery.c.count) / func.count(ReportPost.id)).label(
                "ads_count"
            ),
        )
        .join(subquery, ReportPost.browser_id == subquery.c.id)
        .join(ads_click_subquery, ReportPost.id == ads_click_subquery.c.id)
        .where(
            ReportPost.create.between(start_date, end_date), ReportPost.post_id == id
        )
        .group_by(ReportPost.post_id)
    )
    total = (await db.execute(stmt)).first()
    return {
        "翻页数": total.page_sum,
        "纵深访客数": total.zs_sum,
        "siteId": total.taboola_count,
        "广告点击": total.ads_count,
        "指纹访客": total.browser_count,
        "siteId进入": total.tab_open_sum,
        "IP访客": total.ip_count,
        "总浏览量": total.report_count,
    }


async def get_statistics(db: Session, type, id):
    """
    统计数据
    """
    end_date = datetime.now()
    start_date = datetime.now() - timedelta(days=7)

    if type == "post":
        t = ReportPost.post_id == id
    elif type == "taboola":
        t = ReportPost.taboola_id == id
    elif type == "browser":
        t = ReportPost.browser_id == id

    return {
        "result": await post_statistics(db, id, start_date, end_date),
        "id": 1,
        "total": await post_date_total(db, id, start_date, end_date),
    }


async def taboola_list(session: Session, request_params: TaboolaRequestParams):
    if request_params.domain_id:
        where = Taboola.domain_id == request_params.domain_id
    else:
        where = Taboola.id.in_(
            select(ReportPost.taboola_id)
            .filter(ReportPost.post_id == request_params.post_id)
            .group_by(ReportPost.taboola_id)
        )
    ads_click_subquey = ads_tablie_subquery()
    stmt = (
        select(
            Taboola.id,
            Taboola.site_id,
            Taboola.site,
            Taboola.create,
            func.count(ReportPost.id).label("report_count"),
            func.count(distinct(ReportPost.browser_id)).label("borwser_count"),
            func.count(distinct(ReportPost.visitor_ip)).label("ip_count"),
            (func.sum(ads_click_subquey.c.count) / func.count(ReportPost.id)).label(
                "ads_count"
            ),
            func.sum(cast(ReportPost.is_page, Integer)).label("page_sum"),
            func.sum(case((ReportPost.url.like("%site%"), 1), else_=0)).label(
                "tab_open_sum"
            ),
            func.sum(subquery.c.zs_count).label("zs_sum"),
        )
        .join(ReportPost, ReportPost.taboola_id == Taboola.id)
        .join(ads_click_subquey, ads_click_subquey.c.id == ReportPost.taboola_id)
        .join(subquery, subquery.c.id == ReportPost.browser_id)
        .where(where)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
        .group_by(Taboola.id)
    )

    taboolas: Optional[List] = (await session.execute(stmt)).all()
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
    # print(_orm)
    browsers: Optional[List] = (await session.execute(_orm)).all()

    return browsers


async def reports_list(session: Session, request_params: PostReportRequestParams):
    _orm = (
        select(ReportPost, ReportPost.id, ReportPost.url, ReportPost.create)
        .filter(ReportPost.domain_id == request_params.domain_id)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(request_params.order_by)
    )

    reports: Optional[List] = (await session.execute(_orm)).all()

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
