from pydantic import BaseModel
from typing import Optional

class Msg(BaseModel):
    msg: str
    id: Optional[int]
    show: Optional[bool]