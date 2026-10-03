from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.vehicle import VehicleRead, VehicleCreate, VehicleUpdate

class VehicleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_vehicles(
        self,
        pickup_date: Optional[datetime] = None,
        return_date: Optional[datetime] = None,
        category: Optional[str] = None,
        transmission: Optional[str] = None,
        fuel: Optional[str] = None,
        min_seats: Optional[int] = None,
        max_price: Optional[Decimal] = None,
        location_id: Optional[int] = None,
        sort_by: Optional[str] = None,
        featured_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Vehicle]:
        from sqlalchemy import and_, or_, not_, exists
        from sqlalchemy.orm import selectinload
        from app.models.reservation import Reservation, ReservationStatus

        print("DEBUG: search_vehicles called")
        query = select(Vehicle).options(selectinload(Vehicle.images))

        if pickup_date and return_date:
            print(f"DEBUG: Filtering by dates: {pickup_date} to {return_date}")
            overlap_exists = exists().where(
                and_(
                    Reservation.vehicle_id == Vehicle.id,
                    Reservation.status != ReservationStatus.CANCELLED,
                    Reservation.pickup_datetime < return_date,
                    Reservation.return_datetime > pickup_date
                )
            )
            query = query.where(not_(overlap_exists))

        query = query.where(Vehicle.status == VehicleStatus.AVAILABLE)
        print("DEBUG: Filtered by AVAILABLE status")

        if category:
            query = query.where(Vehicle.category == category)
        if transmission:
            query = query.where(Vehicle.transmission == transmission)
        if fuel:
            query = query.where(Vehicle.fuel == fuel)
        if min_seats:
            query = query.where(Vehicle.seats >= min_seats)
        if max_price:
            query = query.where(Vehicle.daily_price <= max_price)
        if location_id:
            query = query.where(Vehicle.location_id == location_id)
        if featured_only:
            query = query.where(Vehicle.featured == True)

        if sort_by == "price_asc":
            query = query.order_by(Vehicle.daily_price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Vehicle.daily_price.desc())
        elif sort_by == "featured":
            query = query.order_by(Vehicle.featured.desc(), Vehicle.daily_price.asc())
        else:
            query = query.order_by(Vehicle.id.asc())

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        vehicles = result.scalars().all()
        print(f"DEBUG: Found {len(vehicles)} vehicles")
        return vehicles

    async def get_by_slug(self, slug: str) -> Optional[Vehicle]:
        result = await self.session.execute(select(Vehicle).where(Vehicle.slug == slug))
        return result.scalar_one_or_none()

    async def create(self, vehicle_data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(**vehicle_data.model_dump())
        self.session.add(vehicle)
        await self.session.commit()
        await self.session.refresh(vehicle)
        return vehicle

    async def update(self, vehicle_id: int, update_data: VehicleUpdate) -> Optional[Vehicle]:
        vehicle = await self.get_by_id(vehicle_id)
        if not vehicle:
            return None
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(vehicle, key, value)
        await self.session.commit()
        await self.session.refresh(vehicle)
        return vehicle

    async def delete(self, vehicle_id: int) -> bool:
        vehicle = await self.get_by_id(vehicle_id)
        if not vehicle:
            return False
        self.session.delete(vehicle)
        await self.session.commit()
        return True

    async def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        result = await self.session.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
        return result.scalar_one_or_none()
