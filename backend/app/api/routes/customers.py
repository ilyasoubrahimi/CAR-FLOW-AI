from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.api.deps import get_db, get_admin_user
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerRead

router = APIRouter()

@router.get("/", response_model=List[CustomerRead])
async def list_customers(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    # Direct use of session to list all customers
    from app.models.reservation import Customer
    result = await db.execute(select(Customer))
    return result.scalars().all()

@router.post("/", response_model=CustomerRead)
async def create_customer(
    customer_in: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    repo = CustomerRepository(db)
    return await repo.create(customer_in)

@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = CustomerRepository(db)
    customer = await repo.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
