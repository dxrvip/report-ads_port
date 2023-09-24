from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReadTaboola(BaseModel):
    id: int
    site_id: Optional[int]
    site: Optional[str]
    create: Optional[datetime]
    report_count: Optional[int]
    borwser_count: Optional[int]
    ip_count: Optional[int]
    ads_count: Optional[int]
    page_sum: Optional[int]
    tab_open_sum: Optional[int]
    zs_sum: Optional[int]
    hs_sum: Optional[int]
    promotion: Optional[bool]
    class Config:
        orm_mode = True