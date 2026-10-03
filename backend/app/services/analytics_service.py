from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reservation import Reservation, ReservationStatus
from app.models.vehicle import Vehicle

class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_overview(self) -> dict:
        # Total Reservations
        total_res = await self.session.execute(select(func.count(Reservation.id)))
        total_count = total_res.scalar() or 0

        # Confirmed
        conf_res = await self.session.execute(
            select(func.count(Reservation.id)).where(Reservation.status == ReservationStatus.CONFIRMED)
        )
        confirmed_count = conf_res.scalar() or 0

        # Revenue
        rev_res = await self.session.execute(select(func.sum(Reservation.total)))
        total_revenue = rev_res.scalar() or 0.0

        # Active rentals (simplified: confirmed or active)
        active_res = await self.session.execute(
            select(func.count(Reservation.id)).where(
                Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.ACTIVE])
            )
        )
        active_count = active_res.scalar() or 0

        # Most booked vehicles - JOIN with Vehicle table
        most_booked_query = select(
            Vehicle.brand,
            Vehicle.model,
            func.count(Reservation.id).label("count")
        ).join(Vehicle, Reservation.vehicle_id == Vehicle.id).group_by(Vehicle.brand, Vehicle.model).order_by(func.count(Reservation.id).desc()).limit(5)

        most_booked_result = await self.session.execute(most_booked_query)
        most_booked = [{"brand": r[0], "model": r[1], "count": r[2]} for r in most_booked_result.all()]

        return {
            "total_reservations": total_count,
            "today_reservations": 0,
            "confirmed_reservations": confirmed_count,
            "active_rentals": active_count,
            "completed_rentals": 0,
            "cancelled_reservations": 0,
            "total_revenue": float(total_revenue),
            "average_rental_duration": 0.0,
            "most_booked_vehicles": most_booked,
            "available_vehicles": 0,
            "returning_vehicles": 0,
        }
