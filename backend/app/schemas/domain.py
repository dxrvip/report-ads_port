from pydantic import BaseModel, HttpUrl


class DomainCreate(BaseModel):
    base_url: HttpUrl
    pass


class DomainUpdate(DomainCreate):
    pass


class Domain(DomainCreate):

    id:int

    class Config:
        orm_mode = True