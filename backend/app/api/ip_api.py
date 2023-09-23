from fastapi import APIRouter, status
from app.schemas import ip as schemas
from typing import Optional
from app.models.report import VisitorIp
from sqlalchemy import select
from app.deps.db import CurrentAsyncSession
from app.utils.ip_api import IpApi

router = APIRouter(prefix="/ip-pro")


@router.get(
    "/{ip_address}", response_model=schemas.ResultStatu, status_code=status.HTTP_200_OK
)
async def ip_chenck(ip_address: str, session: CurrentAsyncSession):
    visitor_ip: Optional[VisitorIp] = (
        await session.scalars(select(VisitorIp).filter(VisitorIp.ip == ip_address))
    ).first()
    if visitor_ip:
        show = True
        check_ip = IpApi(ip_address=visitor_ip.ip)
        check_ip.get_ip()
        if check_ip.status == "success":
            visitor_ip.hosting = check_ip.hosting
            visitor_ip.proxy = check_ip.proxy
            await session.commit()
            if check_ip.hosting or check_ip.proxy:
                show = False
    return {"msg": check_ip.status, "show": show}
