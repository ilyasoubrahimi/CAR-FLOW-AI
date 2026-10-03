from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db, get_admin_user
from app.repositories.location import LocationRepository
from app.schemas.location import LocationRead, LocationCreate, LocationUpdate

router = APIRouter()

@router.get("/", response_model=List[LocationRead])
async def list_locations(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    repo = LocationRepository(db)
    return await repo.get_all()

@router.post("/", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_in: LocationCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    repo = LocationRepository(db)
    return await repo.create(location_in)

@router.patch("/{location_id}", response_model=LocationRead)
async def update_location(
    location_id: int,
    location_in: LocationUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    repo = LocationRepository(db)
    location = await repo.update(location_id, location_in)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user)
):
    # Safety check: ensure no vehicles or reservations are linked to this location
    # To be implemented fully if requested, but for now let's check if it fails via DB FK
    try:
        repo = LocationRepository(db)
        success = await repo.delete(location_id)
        if not success:
            raise HTTPException(status_code=404, detail="Location not found")
    except Exception as e:
        # SQLAlchemy's IntegrityError (ForeignKeyViolation) will be caught here
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cannot delete location: it is referenced by vehicles or reservations"
        )
    return None
