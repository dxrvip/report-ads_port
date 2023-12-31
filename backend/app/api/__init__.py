from fastapi import APIRouter
from app.api import items, users, utils, domain, report, post,ip_api

api_router = APIRouter()

api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(items.router, tags=["items"]) 
api_router.include_router(domain.router,tags=['domain'])
api_router.include_router(report.router,tags=['report'])
api_router.include_router(post.router,tags=['post'])
api_router.include_router(ip_api.router, tags=['ip-port'])
