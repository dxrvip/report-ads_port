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
    psum: Optional[int] = None
    bsum: Optional[int] = None
    tsum: Optional[int] = None
    rsum: Optional[int] = None
    class Config:
        orm_mode = True

class DomainGetOon(Domain):

    class Config:
        fields = {"sum_posts": {'exclude': True}}