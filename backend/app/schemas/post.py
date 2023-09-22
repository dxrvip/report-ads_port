from datetime import datetime
from pydantic import BaseModel, AnyHttpUrl
from typing import List, Optional, Union


class Post(BaseModel):
    url: str

    class Config:
        orm_mode = True


class Posts(BaseModel):
    id: int = ""
    borwser_count: Optional[int]
    report_count:  Optional[int]
    taboola_count:  Optional[int]
    page_sum: Optional[int]
    zs_sum: Optional[int]
    ip_count: Optional[int]
    tab_open_sum: Optional[int]
    ads_count: Optional[int]
    url:  Optional[str]
    date: Union[datetime, str] = ""


    class Config:
        orm_mode = True


class PostListReport(BaseModel):
    id: int
    url: str
    taboola_count: Optional[int]
    ip_count: Optional[int]
    report_count: Optional[int]
    borwser_count: Optional[int]
    zs_sum: Optional[int]
    page_sum: Optional[int]
    ads_count: Optional[int]
    tab_open_sum: Optional[int]
    promotion: Optional[int]
    create_time: Optional[datetime]
    class Config:
        orm_mode = True


class ReportPost(BaseModel):
    id: int
    result: List[Posts]
    total: Optional[dict]

    class Config:
        orm_mode = True
