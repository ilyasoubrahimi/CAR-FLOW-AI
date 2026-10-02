from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.reservation import Extra
from app.schemas.extra import ExtraCreate, ExtraUpdate

class ExtraRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Extra]:
        result = await self.session.execute(select(Extra))
        return result.scalars().all()

    async def create(self, extra_in: ExtraCreate) -> Extra:
        extra = Extra(**extra_in.model_dump())
        self.session.add(extra)
        await self.session.commit()
        await self.session.refresh(extra)
        return extra

    async def update(self, extra_id: int, update_data: ExtraUpdate) -> Optional[Extra]:
        extra = await self.session.get(Extra, extra_id)
        if not extra:
            return None

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(extra, key, value)

        await self.session.commit()
        await self.session.refresh(extra)
        return extra

    async def delete(self, extra_id: int) -> bool:
        extra = await self.session.get(Extra, extra_id)
        if not extra:
            return False
        self.session.delete(extra)
        await self.session.commit()
        return True
