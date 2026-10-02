from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.availability_service import AvailabilityService
from app.services.pricing_service import PricingService
from app.schemas.availability import AvailabilityRequest, AvailabilityResponse, QuoteRequest, QuoteResponse

router = APIRouter()

@router.post("/check", response_model=AvailabilityResponse)
async def check_availability(
    request: AvailabilityRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AvailabilityService(db)
    available = await service.is_vehicle_available(
        request.vehicle_id,
        request.pickup_datetime,
        request.return_datetime
    )
    return AvailabilityResponse(
        available=available,
        message="Vehicle is available" if available else "Vehicle is already reserved for these dates"
    )

@router.post("/quote", response_model=QuoteResponse)
async def get_quote(
    request: QuoteRequest,
    db: AsyncSession = Depends(get_db)
):
    service = PricingService(db)
    try:
        breakdown = await service.calculate_quote(
            request.vehicle_id,
            request.pickup_datetime,
            request.return_datetime,
            request.extra_ids
        )
        return QuoteResponse(
            subtotal=breakdown.subtotal,
            discount=breakdown.discount,
            extras_total=breakdown.extras_total,
            delivery_fee=breakdown.delivery_fee,
            total=breakdown.total,
            currency=breakdown.currency,
            pricing_breakdown=breakdown.to_dict()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
