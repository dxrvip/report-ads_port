from typing import TYPE_CHECKING, List
from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

if TYPE_CHECKING:
    from app.models.report import Post  # noqa: F401

class Domain(Base):
    __tablename__ = "domain"
    id: Mapped[int] = mapped_column(primary_key=True)
    base_url: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, comment="套利网址")
    create: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="添加时间")
    
    posts: Mapped[List["Post"]] = relationship()

    @hybrid_property
    def sum_posts(self) -> list:
        try:
            total = len(self.posts)
            uv, pv = 0,0
            for item in self.posts:
                # print(item.sum_upv)
                uv = uv + item.sum_upv[0]
                pv = pv + item.sum_upv[1]
            return [total, uv, pv]
        except:
  
            return []