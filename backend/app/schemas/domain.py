from pydantic import BaseModel, HttpUrl
from typing import List
from .report import Post


class DomainCreate(BaseModel):
    base_url: HttpUrl
    pass


class DomainUpdate(DomainCreate):
    pass


class Domain(DomainCreate):

    id:int
    # posts: List[Post]
    sum_posts:list
    class Config:
        orm_mode = True