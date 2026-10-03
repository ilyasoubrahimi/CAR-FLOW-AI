from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime
import uuid
from typing import Optional, List
from app.models.reservation import Reservation, ReservationStatus, ReservationExtra, Extra
from app.models.vehicle import Vehicle, Location
from app.models.reservation import Customer
from app.services.availability_service import AvailabilityService
from app.services.pricing_service import PricingService
from app.services.notification_service import RealNotificationService

class ReservationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.availability_service = AvailabilityService(session)
        self.pricing_service = PricingService(session)
        self.notification_service = RealNotificationService()

    def _generate_reservation_code(self) -> str:
        # Format: MRK-XXXX (e.g., MRK-1042)
        import random
        return f"MRK-{random.randint(1000, 9999)}"

    async def create_draft(self, vehicle_id: int, customer_data: dict, pickup_datetime: datetime, return_datetime: datetime, extra_ids: List[int] = None) -> Reservation:
        # 1. Preliminary Availability Check
        if not await self.availability_service.is_vehicle_available(vehicle_id, pickup_datetime, return_datetime):
            raise ValueError("Vehicle is not available for the selected dates")

        # 2. Handle Customer
        # Check if customer already exists by email
        res_cust = await self.session.execute(select(Customer).where(Customer.email == customer_data.email))
        customer = res_cust.scalar_one_or_none()
        if not customer:
            customer = Customer(
                first_name=customer_data.first_name,
                last_name=customer_data.last_name,
                email=customer_data.email,
                phone=customer_data.phone,
            )
            self.session.add(customer)
            await self.session.flush()

        # 3. Calculate Final Price
        quote = await self.pricing_service.calculate_quote(vehicle_id, pickup_datetime, return_datetime, extra_ids)

        # 4. Determine Locations (use first active location as default)
        loc_res = await self.session.execute(select(Location).where(Location.active == True).limit(1))
        default_location = loc_res.scalar_one_or_none()
        if not default_location:
            raise ValueError("No active rental locations available")

        location_id = default_location.id

        # 5. Create Reservation Object
        reservation = Reservation(
            reservation_code=self._generate_reservation_code(),
            customer_id=customer.id,
            vehicle_id=vehicle_id,
            pickup_location_id=location_id,
            return_location_id=location_id,
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

        # 6. Add Extras
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

        # 7. Notification: Reservation Created (Draft)
        if customer:
            await self.notification_service.send_whatsapp(
                customer.phone,
                f"Hello {customer.first_name}! Your booking request {reservation.reservation_code} for a vehicle has been received. We are processing your request. 🚗"
            )

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
            vehicle = result.scalar()

            # 3. RE-VALIDATE AVAILABILITY while lock is held
            if not await self.availability_service.is_vehicle_available(
                res.vehicle_id, res.pickup_datetime, res.return_datetime, ignore_reservation_id=res.id
            ):
                raise ValueError("Vehicle is no longer available")

            # 4. Update Status
            res.status = ReservationStatus.CONFIRMED
            await self.session.commit()

        # 5. Send Notifications (OUTSIDE the transaction block to avoid closed session errors)
        customer = await self.session.get(Customer, res.customer_id)
        if customer:
            await self.notification_service.send_email(
                customer.email,
                "Reservation Confirmed - Marrakech Drive",
                f"Your reservation {res.reservation_code} is confirmed. We look forward to seeing you!"
            )
            if customer.phone:
                await self.notification_service.send_whatsapp(
                    customer.phone,
                    f"Confirmation: Your Marrakech Drive reservation {res.reservation_code} is confirmed! ✅"
                )

        return res

    async def cancel_reservation(self, reservation_id: int) -> Reservation:
        res = await self.session.get(Reservation, reservation_id)
        if not res:
            raise ValueError("Reservation not found")

        res.status = ReservationStatus.CANCELLED
        await self.session.commit()

        # Notification: Reservation Cancelled
        customer = await self.session.get(Customer, res.customer_id)
        if customer and customer.phone:
            try:
                await self.notification_service.send_whatsapp(
                    customer.phone,
                    f"Hello {customer.first_name}, your Marrakech Drive reservation {res.reservation_code} has been cancelled. ❌"
                )
            except Exception as e:
                logger.error(f"Cancellation notification failed: {str(e)}")

        return res

    async def get_reservation_by_code(self, code: str) -> Optional[Reservation]:
        result = await self.session.execute(select(Reservation).where(Reservation.reservation_code == code))
        return result.scalar_one_or_none()
