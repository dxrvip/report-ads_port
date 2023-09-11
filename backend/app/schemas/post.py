from pydantic import BaseModel, AnyHttpUrl


class Post(BaseModel):
    url: str
    class Config:
        orm_mode = True
        
class Posts(BaseModel):
    bsum: int
    rsum: int
    tsum: int
    url: str
    id: int
    class Config:
        orm_mode = True
