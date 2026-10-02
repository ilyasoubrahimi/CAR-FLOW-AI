from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.reservation import Customer
from app.schemas.customer import CustomerCreate, CustomerRead

class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, customer_in: CustomerCreate) -> Customer:
        # Check if customer already exists by email or phone
        result = await self.session.execute(
            select(Customer).where(
                (Customer.email == customer_in.email) |
                (Customer.phone == customer_in.phone)
            )
        )
        customer = result.scalar_one_or_none()

        if not customer:
            customer = Customer(**customer_in.model_dump())
            self.session.add(customer)
            await self.session.commit()
            await self.session.refresh(customer)

        return customer

    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return await self.session.get(Customer, customer_id)
