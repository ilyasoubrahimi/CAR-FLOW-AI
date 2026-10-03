from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_admin_user
from app.repositories.extra import ExtraRepository
from app.schemas.extra import ExtraRead, ExtraCreate, ExtraUpdate

router = APIRouter()

@router.get('/', response_model=List[ExtraRead])
async def get_extras(db: AsyncSession = Depends(get_db)):
    repo = ExtraRepository(db)
    return await repo.get_all()

@router.post('/', response_model=ExtraRead, status_code=status.HTTP_201_CREATED)
async def create_extra(
    extra_in: ExtraCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    repo = ExtraRepository(db)
    return await repo.create(extra_in)

@router.patch('/{extra_id}', response_model=ExtraRead)
async def update_extra(
    extra_id: int,
    extra_in: ExtraUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    repo = ExtraRepository(db)
    extra = await repo.update(extra_id, extra_in)
    if not extra:
        raise HTTPException(status_code=404, detail='Extra not found')
    return extra

@router.delete('/{extra_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_extra(
    extra_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    repo = ExtraRepository(db)
    success = await repo.delete(extra_id)
    if not success:
        raise HTTPException(status_code=404, detail='Extra not found')
    return None
