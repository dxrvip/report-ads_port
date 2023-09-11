from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class ReportCreate(BaseModel):
    fingerprint_id: str



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


class Report(BaseModel):
    id: int
    url: str
    create: datetime
    is_page: bool
    browser_info: BrowserInfo
    visitor: VisitorIp

    class Config:
        orm_mode = True


class Taboola(BaseModel):
    site: str
    site_id: int
    click_id: str
    campaign_item_id: str
    campaign_id: int
    platform: str

    class Config:
        orm_mode = True


class ResultTaboola(BaseModel):
    id: int
    site_id: int
    platform: str
    psum: int
    rsum: int
    class Config:
        orm_mode = True

class ResultReport(BaseModel):
    id: int
    url: str
    create: datetime

    class Config:
        orm_mode = True


class ResultBrowserInfo(BaseModel):
    id:int
    psum: int
    rsum: int
    user_agent: str
    update_time: datetime
    class Config:
        orm_mode = True