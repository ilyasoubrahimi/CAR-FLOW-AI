from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.vehicle import Company
from app.schemas.company import CompanyUpdate

class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_company(self) -> Optional[Company]:
        # We assume there is only one active company for the instance
        result = await self.session.execute(select(Company))
        return result.scalars().first()

    async def update_company(self, company_id: int, update_data: CompanyUpdate) -> Optional[Company]:
        company = await self.session.get(Company, company_id)
        if not company:
            return None

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)

        await self.session.commit()
        await self.session.refresh(company)
        return company
