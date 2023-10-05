from fastapi import APIRouter, Header, status
from app.schemas import ip as schemas
from typing import Optional
from app.models.report import VisitorIp
from sqlalchemy import select
from app.deps.db import CurrentAsyncSession
from app.utils.ip_api import IpApi

router = APIRouter(prefix="/ip-pro")


@router.get("", response_model=schemas.ResultStatu, status_code=status.HTTP_200_OK)
async def ip_chenck(
    session: CurrentAsyncSession,
    cf_connecting_ip: Optional[str] = Header(None),
):
    show, onl_ip = True, False
    visitor_ip: Optional[VisitorIp] = (
        await session.scalars(
            select(VisitorIp).filter(VisitorIp.ip == cf_connecting_ip)
        )
    ).first()
    if visitor_ip is None:
        onl_ip = True
        visitor_ip = VisitorIp(ip=cf_connecting_ip)
        session.add(visitor_ip)
        await session.commit()

    check_ip = IpApi(ip_address=visitor_ip.ip)
    check_ip.get_ip()
    if check_ip.status == "success":
        visitor_ip.hosting = check_ip.hosting
        visitor_ip.proxy = check_ip.proxy
        await session.commit()
        if check_ip.hosting or check_ip.proxy:
            show = False
    return {"msg": check_ip.status, "show": show, "onl_ip": onl_ip}
