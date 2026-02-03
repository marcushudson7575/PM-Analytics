"""
API v1 router - combines all endpoint routers.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import funds, analytics

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(funds.router)
api_router.include_router(analytics.router)
