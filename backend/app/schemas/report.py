from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ReportCreate(BaseModel):
    fingerprint_id: Optional[str]
    site_id: Optional[int]
    campaign_id: Optional[int]
    campaign_item_id: Optional[str]


class TongjiCreate(BaseModel):
    referrer: Optional[str]
    url: Optional[str]
    class Config:
        orm_mode: True


class Post(BaseModel):
    id: int
    slug: str

    # sum_upv: tuple
    class Config:
        orm_mode = True


class BrowserInfo(BaseModel):
    fingerprint_id: str
    equipment: dict

    class Config:
        orm_mode = True


class VisitorIp(BaseModel):
    ip: str

    class Config:
        orm_mode = True


class Taboola(BaseModel):
    site: str
    site_id: int
    click_id: str
    platform: str

    class Config:
        orm_mode = True


class Report(BaseModel):
    id: int
    url: str
    create: datetime
    browser_info: Optional[BrowserInfo]
    visitor: Optional[VisitorIp]
    taboola_info: Optional[Taboola]
    taboola_id: Optional[int]

    class Config:
        orm_mode = True


class ResultTaboola(BaseModel):
    id: int
    site_id: Optional[int]
    page_sum: Optional[int]
    post_sum: Optional[int]
    report_sum: Optional[int]
    ip_sum: Optional[int]
    zs_sum: Optional[int]
    create: Optional[datetime]
    promotion: Optional[bool]

    class Config:
        orm_mode = True


class ResultReport(BaseModel):
    id: int
    url: str
    create: datetime

    class Config:
        orm_mode = True


class ResultBrowserInfo(BaseModel):
    id: int
    psum: int
    rsum: int
    user_agent: str
    update_time: datetime

    class Config:
        orm_mode = True
