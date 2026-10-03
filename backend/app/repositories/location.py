from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models.vehicle import Location
from app.schemas.location import LocationCreate, LocationUpdate

class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, active_only: bool = False):
        query = select(Location)
        if active_only:
            query = query.where(Location.active == True)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, location_id: int):
        return await self.session.get(Location, location_id)

    async def create(self, data: LocationCreate):
        location = Location(**data.model_dump())
        self.session.add(location)
        await self.session.commit()
        await self.session.refresh(location)
        return location

    async def update(self, location_id: int, data: LocationUpdate):
        location = await self.get_by_id(location_id)
        if not location:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(location, field, value)
        
        await self.session.commit()
        await self.session.refresh(location)
        return location

    async def delete(self, location_id: int):
        location = await self.get_by_id(location_id)
        if not location:
            return False
        
        await self.session.delete(location)
        await self.session.commit()
        return True
