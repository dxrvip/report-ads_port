from datetime import datetime
from pydantic import BaseModel, AnyHttpUrl
from typing import List, Optional, Union


class Post(BaseModel):
    url: str

    class Config:
        orm_mode = True


class Posts(BaseModel):
    id: int = ""
    bsum: int
    rsum: int
    tsum: int
    url: str = ""
    date: Union[datetime, str] = ""
    psum: str = 0

    class Config:
        orm_mode = True


class PostListReport(BaseModel):
    id: int
    url: str
    tsum: int
    bsum: int
    rsum: int

    class Config:
        orm_mode = True


class ReportPost(BaseModel):
    id: int
    result: List[Posts]
    total: dict

    class Config:
        orm_mode = True
