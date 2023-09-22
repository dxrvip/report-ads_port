from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime
from .report import Post


class DomainCreate(BaseModel):
    base_url: HttpUrl
    pass


class DomainUpdate(DomainCreate):
    pass


class Domain(DomainCreate):

    id:int
    create: datetime
    post_count: Optional[int] = None
    report_count: Optional[int]
    browser_count: Optional[int]
    taboola_count: Optional[int] 
    ip_count: Optional[int]
    class Config:
        orm_mode = True

class DomainGetOon(Domain):

    class Config:
        fields = {"sum_posts": {'exclude': True}}