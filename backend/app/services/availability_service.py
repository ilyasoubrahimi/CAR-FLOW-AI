from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models.reservation import Reservation, ReservationStatus
from app.models.vehicle import Vehicle

class AvailabilityService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_vehicle_available(self, vehicle_id: int, pickup_date: datetime, return_date: datetime) -> bool:
        """
        A vehicle is unavailable if there is any reservation that:
        1. Is not CANCELLED
        2. Overlaps with the requested date range
        """
        # Overlap logic: (StartA < EndB) AND (EndA > StartB)
        query = select(Reservation).where(
            and_(
                Reservation.vehicle_id == vehicle_id,
                Reservation.status != ReservationStatus.CANCELLED,
                Reservation.pickup_datetime < return_date,
                Reservation.return_datetime > pickup_date
            )
        )

        result = await self.session.execute(query)
        overlapping_reservations = result.scalars().all()

        return len(overlapping_reservations) == 0

    async def get_available_vehicles(self, pickup_date: datetime, return_date: datetime, category: str = None) -> list[Vehicle]:
        """
        Finds all vehicles that do not have overlapping reservations for the period.
        Optimized using a NOT EXISTS subquery.
        """
        from app.models.reservation import Reservation
        from sqlalchemy import exists

        # Subquery: check if any reservation exists for the vehicle that overlaps
        overlap_exists = exists().where(
            and_(
                Reservation.vehicle_id == Vehicle.id,
                Reservation.status != ReservationStatus.CANCELLED,
                Reservation.pickup_datetime < return_date,
                Reservation.return_datetime > pickup_date
            )
        )

        query = select(Vehicle).where(
            and_(
                Vehicle.status == "AVAILABLE",
                ~overlap_exists
            )
        )

        if category:
            query = query.where(Vehicle.category == category)

        result = await self.session.execute(query)
        return result.scalars().all()
