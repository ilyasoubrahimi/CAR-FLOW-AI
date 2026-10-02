from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.reservation_service import ReservationService
from app.schemas.reservation import ReservationCreate, ReservationRead

router = APIRouter()

@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    request: ReservationCreate,
    db: AsyncSession = Depends(get_db)
):
    service = ReservationService(db)
    try:
        return await service.create_draft(
            request.vehicle_id,
            request.customer_id,
            request.pickup_datetime,
            request.return_datetime,
            request.extra_ids
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{res_id}/confirm", response_model=ReservationRead)
async def confirm_reservation(
    res_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = ReservationService(db)
    try:
        return await service.confirm_reservation(res_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{code}", response_model=ReservationRead)
async def get_reservation(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    service = ReservationService(db)
    res = await service.get_reservation_by_code(code)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return res

@router.post("/{res_id}/cancel", response_model=ReservationRead)
async def cancel_reservation(
    res_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = ReservationService(db)
    try:
        return await service.cancel_reservation(res_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
