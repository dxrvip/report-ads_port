from pydantic import BaseModel
from typing import Optional

class ResultStatu(BaseModel):

    msg: Optional[str]
    show: bool = False
    onl_ip: Optional[bool]
    class Config:
        orm_mode = True