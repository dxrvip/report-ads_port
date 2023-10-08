from ast import List
from typing import Optional
from sqlalchemy import DATE, and_, case, desc, select, func, distinct, cast, Integer
from sqlalchemy.orm import Session
from app.models.report import ReportPost, AdsClick, ItemStatus

from app.deps.request_params import ItemRequestParams
from app.crud.post import subquery


async def get_item_list(db: Session, request_params: ItemRequestParams):
    tab_open_sum = case(
        (
            and_(
                func.sum(case((ReportPost.url.like("%site%"), 1), else_=0)) > 0,
                func.count(distinct(AdsClick.id)) > 0,
            ),
            func.sum(case((ReportPost.url.like("%site%"), 1), else_=0))
            / func.count(distinct(AdsClick.id)),
        ),
        else_=func.sum(case((ReportPost.url.like("%site%"), 1), else_=0)),
    ).label("tab_open_sum")
    zs_site_open = (
        case(
            (
                and_(
                    func.count(distinct(subquery.c.zs_count)) > 0,
                    tab_open_sum > 0,
                ),
                func.count(distinct(subquery.c.zs_count)) / tab_open_sum,
            ),
            else_=0,
        )
    ).label("zs_site_open")
    page_sum = case(
        (
            and_(
                func.sum(cast(ReportPost.is_page, Integer)) > 0,
                func.count(distinct(AdsClick.id)) > 0,
            ),
            func.sum(cast(ReportPost.is_page, Integer))
            / func.count(distinct(AdsClick.id)),
        ),
        else_=func.sum(cast(ReportPost.is_page, Integer)),
    ).label("page_sum")
    page_zs = (
        case(
            (
                and_(page_sum > 0, tab_open_sum > 0),
                page_sum / tab_open_sum,
            ),
            else_=0,
        )
    ).label("page_zs")
    ads_show_sum = case(
        (
            and_(
                func.sum(cast(ReportPost.ads_show_sum, Integer)) > 0,
                func.count(distinct(AdsClick.id)) > 0,
            ),
            func.sum(cast(ReportPost.ads_show_sum, Integer))
            / func.count(distinct(AdsClick.id)),
        ),
        else_=func.sum(cast(ReportPost.ads_show_sum, Integer)),
    ).label("ads_show_sum")

    stmt = (
        select(
            ReportPost.campaign_item_id.label('id'),
            ReportPost.campaign_id,
            ItemStatus.status,
            func.count(ReportPost.campaign_item_id).label("report_count"),
            func.count(distinct(ReportPost.taboola_id)).label("taboola_count"),
            func.count(distinct(ReportPost.browser_id)).label("borwser_count"),
            func.count(distinct(ReportPost.visitor_ip)).label("ip_count"),
            func.count(distinct(AdsClick.id)).label("ads_count"),
            func.count(distinct(subquery.c.zs_count)).label("zs_sum"),
            func.count(distinct(ReportPost.campaign_item_id)).label("item_count"),
            page_zs,
            ads_show_sum,
            zs_site_open,
            page_sum,
            tab_open_sum,
        )
        .filter_by(**request_params.filters.dict(exclude_unset=True, exclude={'create_time'}))
        .join(subquery, ReportPost.browser_id == subquery.c.id)
        .outerjoin(AdsClick, AdsClick.post_id == ReportPost.post_id)
        .outerjoin(ItemStatus, ItemStatus.campaign_item_id==ReportPost.campaign_item_id)
        .offset(request_params.skip)
        .limit(request_params.limit)
        .order_by(desc(ReportPost.campaign_item_id))
        .group_by(ReportPost.campaign_item_id, ItemStatus.status, ReportPost.campaign_id)
        
    )
    if request_params.filters.create_time:
        stmt = stmt.filter(
            cast(ReportPost.create, DATE)
            == cast(request_params.filters.create_time, DATE)
        )
    # print(stmt)
    item: Optional[List] = (await db.execute(stmt)).all()
    return item
