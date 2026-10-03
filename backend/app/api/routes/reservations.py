from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
from app.api.deps import get_db, get_admin_user
from app.services.reservation_service import ReservationService
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.models.reservation import Reservation

router = APIRouter()

@router.get("/", response_model=List[ReservationRead])
async def list_reservations(
    status: Optional[str] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    # Note: ReservationService currently doesn't have a list method with filters.
    # We will use the session directly for this admin view.
    query = select(Reservation)
    if status:
        query = query.where(Reservation.status == status)
    if vehicle_id:
        query = query.where(Reservation.vehicle_id == vehicle_id)

    result = await db.execute(query)
    return result.scalars().all()

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
