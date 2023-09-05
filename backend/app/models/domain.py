from typing import TYPE_CHECKING
from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql.functions import func
from datetime import datetime


class Domain(Base):
    __tablename__ = "domain"
    id: Mapped[int] = mapped_column(primary_key=True)
    base_url: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, comment="套利网址")
    create: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="添加时间")
    