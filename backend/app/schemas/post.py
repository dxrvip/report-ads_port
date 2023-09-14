from datetime import datetime
from pydantic import BaseModel, AnyHttpUrl
from typing import List


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
    date: datetime = None
    psum: str = 0

    class Config:
        orm_mode = True




class ReportPost(BaseModel):
    id: int
    result: List[Posts]
    total: dict

    class Config:
        orm_mode = True
