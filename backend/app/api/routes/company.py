from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_admin_user
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyRead, CompanyUpdate
from app.models.vehicle import Company

router = APIRouter()

@router.get("/", response_model=CompanyRead)
async def get_company_settings(
    db: AsyncSession = Depends(get_db)
):
    repo = CompanyRepository(db)
    company = await repo.get_active_company()
    if not company:
        raise HTTPException(status_code=404, detail="Company configuration not found")
    return company

@router.patch("/", response_model=CompanyRead)
async def update_company_settings(
    update_data: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    repo = CompanyRepository(db)
    company = await repo.get_active_company()
    if not company:
        raise HTTPException(status_code=404, detail="Company configuration not found")

    updated_company = await repo.update_company(company.id, update_data)
    return updated_company
