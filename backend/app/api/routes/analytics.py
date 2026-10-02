from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_admin_user
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsOverview

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    service = AnalyticsService(db)
    return await service.get_overview()
