from pydantic import BaseModel
from typing import Optional

class ResultStatu(BaseModel):

    msg: Optional[str]
    show: bool = False

    class Config:
        orm_mode = True