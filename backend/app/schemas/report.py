from pydantic import BaseModel
from datetime import datetime


class ReportCreate(BaseModel):
    fingerprint_id: str


class Post(BaseModel):
    id: int
    slug: str
    class Config:
        orm_mode = True
class Report(BaseModel):
    id: int
    url: str
    create: datetime
    is_page: bool
    post: Post
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
