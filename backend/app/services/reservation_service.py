from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime
import uuid
from typing import Optional, List
from app.models.reservation import Reservation, ReservationStatus, ReservationExtra, Extra
from app.models.vehicle import Vehicle
from app.models.customer import Customer
from app.services.availability_service import AvailabilityService
from app.services.pricing_service import PricingService

class ReservationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.availability_service = AvailabilityService(session)
        self.pricing_service = PricingService(session)

    def _generate_reservation_code(self) -> str:
        # Format: MRK-XXXX (e.g., MRK-1042)
        import random
        return f"MRK-{random.randint(1000, 9999)}"

    async def create_draft(self, vehicle_id: int, customer_id: int, pickup_datetime: datetime, return_datetime: datetime, extra_ids: List[int] = None) -> Reservation:
        # 1. Preliminary Availability Check
        if not await self.availability_service.is_vehicle_available(vehicle_id, pickup_datetime, return_datetime):
            raise ValueError("Vehicle is not available for the selected dates")

        # 2. Calculate Final Price
        quote = await self.pricing_service.calculate_quote(vehicle_id, pickup_datetime, return_datetime, extra_ids)

        # 3. Create Reservation Object
        reservation = Reservation(
            reservation_code=self._generate_reservation_code(),
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            pickup_location_id=1, # Default to first location for now
            return_location_id=1,
            pickup_datetime=pickup_datetime,
            return_datetime=return_datetime,
            status=ReservationStatus.DRAFT,
            subtotal=quote.subtotal,
            discount=quote.discount,
            extras_total=quote.extras_total,
            delivery_fee=quote.delivery_fee,
            total=quote.total,
            currency=quote.currency
        )

        self.session.add(reservation)
        await self.session.flush() # Get reservation ID

        # 4. Add Extras
        if extra_ids:
            for eid in extra_ids:
                # Fetch current price of extra for the record
                res = await self.session.execute(select(Extra).where(Extra.id == eid))
                extra = res.scalar_one()
                res_extra = ReservationExtra(
                    reservation_id=reservation.id,
                    extra_id=eid,
                    price_at_booking=extra.price
                )
                self.session.add(res_extra)

        await self.session.commit()
        return reservation

    async def confirm_reservation(self, reservation_id: int) -> Reservation:
        # Use a transaction with SELECT FOR UPDATE to lock the vehicle and prevent concurrent bookings
        async with self.session.begin():
            # 1. Fetch Reservation
            res = await self.session.get(Reservation, reservation_id)
            if not res:
                raise ValueError("Reservation not found")

            if res.status != ReservationStatus.DRAFT:
                raise ValueError("Only DRAFT reservations can be confirmed")

            # 2. LOCK the vehicle row to prevent concurrent modifications
            # This prevents race conditions where two users confirm the same vehicle
            stmt = select(Vehicle).where(Vehicle.id == res.vehicle_id).with_for_update()
            result = await self.session.execute(stmt)
            await result.scalar()

            # 3. RE-VALIDATE AVAILABILITY while lock is held
            if not await self.availability_service.is_vehicle_available(res.vehicle_id, res.pickup_datetime, res.return_datetime):
                raise ValueError("Vehicle is no longer available")

            # 4. Update Status
            res.status = ReservationStatus.CONFIRMED
            await self.session.commit()
            return res

    async def cancel_reservation(self, reservation_id: int) -> Reservation:
        res = await self.session.get(Reservation, reservation_id)
        if not res:
            raise ValueError("Reservation not found")

        res.status = ReservationStatus.CANCELLED
        await self.session.commit()
        return res

    async def get_reservation_by_code(self, code: str) -> Optional[Reservation]:
        result = await self.session.execute(select(Reservation).where(Reservation.reservation_code == code))
        return result.scalar_one_or_none()
