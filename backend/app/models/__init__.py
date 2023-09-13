# Import all models here so alembic can discover them
from app.models.item import Item
from app.models.user import User
from app.models.domain import Domain
from app.models.report import ReportPost, Post, VisitorIp, BrowserInfo, Taboola

# from app.models.report import Post