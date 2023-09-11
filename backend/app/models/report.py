from typing import TYPE_CHECKING, List
from app.db import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from user_agents import parse
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, ForeignKey, String, Boolean, Integer, Table
from sqlalchemy.sql.sqltypes import DateTime

# if TYPE_CHECKING:
#     from app.models.domain import Domain

class ReportPost(Base):
    __tablename__ = "report"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, nullable=False, comment="推广网址")
    is_page: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否翻页")
    create: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="添加时间")
    
    post_id: Mapped[int | None] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="report_post")

    visitor_ip: Mapped[int] = mapped_column(ForeignKey("visitor_ip.id"))
    visitor: Mapped["VisitorIp"] = relationship(back_populates="report_post")

    browser_id: Mapped[int] = mapped_column(ForeignKey("browser_info.id"))
    browser_info: Mapped["BrowserInfo"] = relationship(back_populates="report")

    domain_id: Mapped[id] = mapped_column(ForeignKey("domain.id"), nullable=True, server_default=None)

    """https://www.xiaoganxw.info/the-22-funny-cartoons-i-made-convey-the-message-in-a-few-words?
    utm_source=Taboola&
    campaign_item_id=3720063430
    &site=izooto-sea-premium
    &site_id=1591683
    &campaign_id=26634621
    &platform=Other
    &click_id=GiCOLHrFCBOaAq-FneZKR0PB85RoNyeTMsNeyPXd8gZUriCDk2EostDKi4Pe_oPNAQ"""

# 外键
post_taboola_table = Table(
    "post_taboola_table",
    Base.metadata,
    Column("id", primary_key=True),
    Column("post_id", ForeignKey("post.id"), index=True),
    Column("taboola_id", ForeignKey("taboola.id"), index=True)
)

class Taboola(Base):
    __tablename__ = "taboola"

    id: Mapped[int] = mapped_column(primary_key=True)
    site: Mapped[str] = mapped_column(String(200), nullable=True) # 发布者网站或应用程序名称。
    site_id: Mapped[int] = mapped_column(Integer, nullable=False) # 发布商网站或应用程序的唯一 Taboola 网站 ID。
    click_id: Mapped[str] = mapped_column(String(100), nullable=False) #
    campaign_item_id: Mapped[str] = mapped_column(String(15), nullable=False) # 唯一的 Taboola 项目 ID，如 Backstage 中的“热门营销活动内容”报告中所定义。
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False) # 唯一的 Taboola 活动 ID。该活动ID也可以在后台的“活动管理”页面找到。
    platform: Mapped[str] = mapped_column(String(30), nullable=True) #  展示您的商品的用户平台。这将返回为“桌面”、“移动设备”或“平板电脑”。

    posts: Mapped[List["Post"]] = relationship(secondary=post_taboola_table, back_populates="taboolas")

    domain_id: Mapped[id] = mapped_column(ForeignKey("domain.id"), nullable=True, server_default=None)

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="推广网址")
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    report_post: Mapped[List["ReportPost"]] = relationship(back_populates="post")
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    browser_info: Mapped[List["BrowserInfo"]] = relationship() 
    taboolas: Mapped[List[Taboola]] = relationship(secondary=post_taboola_table, back_populates="posts")

    domain_id: Mapped[id] = mapped_column(ForeignKey("domain.id"), nullable=True, server_default=None)

    @hybrid_property
    def sum_upv(self)-> tuple:
        return (len(self.browser_info), len(self.report_post))

class BrowserInfo(Base):
    """访客唯一特征标记表"""
    __tablename__ = "browser_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fingerprint_id: Mapped[str] = mapped_column(String(15), nullable=False, comment="指纹ID", index=True)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False, comment="浏览器ua")
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="访问时间")
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    post_id: Mapped[int | None] = mapped_column(ForeignKey("post.id"), comment="帖子信息")

    report: Mapped["ReportPost"] = relationship(back_populates="browser_info")

    domain_id: Mapped[id] = mapped_column(ForeignKey("domain.id"), nullable=True, server_default=None)
    
    @hybrid_property
    def equipment(self) -> dict:
        try:
            print(self.user_agent)
            user_agent = parse(self.user_agent)
            return {"browser": user_agent.browser, "os": user_agent.os, "is_bot": user_agent.is_bot, "device": user_agent.device}
        except:
            return {}

class VisitorIp(Base):
    """访问ip记录表"""
    __tablename__ = "visitor_ip"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip: Mapped[str] = mapped_column(String(20), nullable=False, comment="访客ip")

    report_post: Mapped["ReportPost"] = relationship(back_populates="visitor")