from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ItemCreate(BaseModel):
    # value: str
    pass


class ItemUpdate(ItemCreate):
    pass


class Item(ItemCreate):
    taboola_count: Optional[int]
    ip_count: Optional[int]
    report_count: Optional[int]
    borwser_count: Optional[int]
    zs_sum: Optional[int]
    page_sum: Optional[int]
    ads_count: Optional[int]
    tab_open_sum: Optional[int]
    promotion: Optional[int]
    create: Optional[datetime]
    id: Optional[int]
    page_zs: Optional[float]
    zs_site_open: Optional[float]
    ads_show_sum: Optional[int] = 0
    item_count: Optional[int]
    item_status: Optional[int]
    item_status_count: Optional[int]
    status: Optional[bool]
    class Config:
        orm_mode = True
