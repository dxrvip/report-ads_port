from typing import TYPE_CHECKING, List
from app.db import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from user_agents import parse
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import Column, ForeignKey, String, Boolean, Integer, Table, SmallInteger
from sqlalchemy.sql.sqltypes import DateTime

# if TYPE_CHECKING:
#     from app.models.domain import Domain


class ReportPost(Base):
    __tablename__ = "report"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, nullable=False, comment="推广网址")
    is_page: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="是否翻页"
    )
    create: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="添加时间"
    )

    post_id: Mapped[int | None] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="report_post")

    visitor_ip: Mapped[int] = mapped_column(ForeignKey("visitor_ip.id"))
    visitor: Mapped["VisitorIp"] = relationship(back_populates="report_post")

    browser_id: Mapped[int] = mapped_column(ForeignKey("browser_info.id"))
    browser_info: Mapped["BrowserInfo"] = relationship(back_populates="report")

    taboola_id: Mapped[int] = mapped_column(
        ForeignKey("taboola.id"), nullable=True, server_default=None
    )
    taboola_info: Mapped["Taboola"] = relationship(back_populates="reports")

    domain_id: Mapped[id] = mapped_column(
        ForeignKey("domain.id"), nullable=True, server_default=None
    )

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
    # Column("id", primary_key=True, autoincrement=True),
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("taboola_id", ForeignKey("taboola.id"), primary_key=True),
    Column("create", DateTime(timezone=True), server_default=func.now()),
)
# 外键
post_browser_table = Table(
    "post_browser_table",
    Base.metadata,
    # Column("id", primary_key=True, autoincrement=True),
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("browser_id", ForeignKey("browser_info.id"), primary_key=True),
    Column("create", DateTime(timezone=True), server_default=func.now()),
)


class Taboola(Base):
    __tablename__ = "taboola"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site: Mapped[str] = mapped_column(String(200), nullable=True)  # 发布者网站或应用程序名称。
    site_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True
    )  # 发布商网站或应用程序的唯一 Taboola 网站 ID。
    click_id: Mapped[str] = mapped_column(String(100), nullable=False)  #
    campaign_item_id: Mapped[str] = mapped_column(
        String(15), nullable=False
    )  # 唯一的 Taboola 项目 ID，如 Backstage 中的“热门营销活动内容”报告中所定义。
    campaign_id: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # 唯一的 Taboola 活动 ID。该活动ID也可以在后台的“活动管理”页面找到。
    platform: Mapped[str] = mapped_column(
        String(200), nullable=True
    )  #  展示您的商品的用户平台。这将返回为“桌面”、“移动设备”或“平板电脑”。
    create: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="添加时间"
    )

    posts: Mapped[List["Post"]] = relationship(
        secondary=post_taboola_table, back_populates="taboolas"
    )

    reports: Mapped[List["ReportPost"]] = relationship(back_populates="taboola_info")


    promotion: Mapped[int] = mapped_column(SmallInteger,nullable=True,comment="停止推广")
    # @hybrid_property
    # def _platform(self):
    #     print(self._platform)
    #     pass
        # if(self._platform in 'Other'):
        #     return "其他"
        # elif(self._platform in "Smartphone"):
        #     return "手机"
        # print(self._platform)
        # return self._platform

    """ SQL: INSERT INTO taboola (site, site_id, click_id, campaign_item_id, campaign_id, platform, domain_id, promotion) VALUES ($1::VARCHAR, $2::INTEGER, $3::VARCHAR, $4::VARCHAR, $5::INTEGER, $6::VARCHAR, $7::INTEGER, $8::INTEGER) RETURNING taboola.id, taboola."create"]
report-ads_port-backend-1   | 
2023-09-16T13:58:24.308198425Z  'jagrannewmedia-jagranjosh', 1450019, 'GiCvf7gfZI2-U0jKxVftC6x35t2m9YoVA8GYzgxiTiLUDiCDk2Eov4D15t2DtIk4', '3731643422', 27592825, 'Smartphone#tblciGiCvf7gfZI2-U0jKxVftC6x35t2m9YoVA8GYzgxiTiLUDiCDk2Eov4D15t2DtIk4', 2, None)]
report-ads_port-backend-1   | 
2023-09-16T13:58:24.308200419Z     | (Background on this error at: https://sqlalche.me/e/20/dbapi)
"""
    #https://www.pmsnhu.com/the-foods-that-could-make-you-want-run-for-the-hills?utm_source=Taboola&campaign_item_id=3731643422&site=jagrannewmedia-jagranjosh&site_id=1450019&campaign_id=27592825&platform=Smartphone&click_id=GiCvf7gfZI2-U0jKxVftC6x35t2m9YoVA8GYzgxiTiLUDiCDk2Eov4D15t2DtIk4
  


class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="推广网址"
    )
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    report_post: Mapped[List["ReportPost"]] = relationship(back_populates="post")

    browser_info: Mapped[List["BrowserInfo"]] = relationship(
        secondary=post_browser_table, back_populates="posts"
    )
    taboolas: Mapped[List["Taboola"]] = relationship(
        secondary=post_taboola_table, back_populates="posts"
    )

    domain_id: Mapped[id] = mapped_column(
        ForeignKey("domain.id"), nullable=True, server_default=None
    )

    promotion: Mapped[int] = mapped_column(SmallInteger,nullable=True,comment="停止推广")
    # @hybrid_property
    # def sum_upv(self)-> tuple:
    #     return (len(self.browser_info), len(self.report_post))


class BrowserInfo(Base):
    """访客唯一特征标记表"""

    __tablename__ = "browser_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fingerprint_id: Mapped[str] = mapped_column(
        String(15), unique=False, nullable=False, comment="指纹ID", index=True
    )
    user_agent: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="浏览器ua"
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="访问时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    posts: Mapped[List["Post"]] = relationship(
        secondary=post_browser_table, back_populates="browser_info"
    )

    report: Mapped["ReportPost"] = relationship(back_populates="browser_info")


    @hybrid_property
    def equipment(self) -> dict:
        try:
            print(self.user_agent)
            user_agent = parse(self.user_agent)
            return {
                "browser": user_agent.browser,
                "os": user_agent.os,
                "is_bot": user_agent.is_bot,
                "device": user_agent.device,
            }
        except:
            return {}


class VisitorIp(Base):
    """访问ip记录表"""

    __tablename__ = "visitor_ip"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, comment="访客ip"
    )

    report_post: Mapped["ReportPost"] = relationship(back_populates="visitor")
