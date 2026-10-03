from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.payment_service import MockPaymentService, PaymentRequest
from app.models.reservation import Reservation
from sqlalchemy.future import select
from datetime import datetime
from decimal import Decimal

router = APIRouter()

# Use Mock for recording payment status (Pay at Pickup)
payment_provider = MockPaymentService()

@router.post("/intent", response_model=str)
async def create_payment_intent(
    reservation_id: int,
    amount: float,
    payment_method: str,
    db: AsyncSession = Depends(get_db)
):
    res = await db.get(Reservation, reservation_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")

    request = PaymentRequest(
        reservation_id=reservation_id,
        amount=Decimal(str(amount)),
        payment_method=payment_method
    )

    return await payment_provider.create_payment_intent(request)

@router.post("/confirm", response_model=dict)
async def confirm_payment(
    transaction_id: str,
    reservation_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        payment_res = await payment_provider.confirm_payment(transaction_id)

        if payment_res.status != payment_res.status.PAID:
             raise HTTPException(status_code=400, detail="Payment not confirmed")

        res = await db.get(Reservation, reservation_id)
        if not res:
            raise HTTPException(status_code=404, detail="Reservation not found")

        from app.models.reservation import ReservationStatus
        res.status = ReservationStatus.CONFIRMED

        await db.commit()
        return {"status": "success", "reservation_code": res.reservation_code}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
