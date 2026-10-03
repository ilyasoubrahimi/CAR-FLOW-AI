from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from app.api.deps import get_db
from app.repositories.vehicle import VehicleRepository
from app.schemas.vehicle import VehicleRead, VehicleCreate, VehicleUpdate, VehicleDiscoveryResponse

router = APIRouter()

@router.get("/", response_model=VehicleDiscoveryResponse)
async def read_vehicles(
    pickup_date: Optional[datetime] = Query(None),
    return_date: Optional[datetime] = Query(None),
    category: Optional[str] = Query(None),
    transmission: Optional[str] = Query(None),
    fuel: Optional[str] = Query(None),
    min_seats: Optional[int] = Query(None),
    max_price: Optional[Decimal] = Query(None),
    location_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("featured"),
    featured_only: bool = Query(False),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    print("DEBUG: read_vehicles route called")
    repo = VehicleRepository(db)
    vehicles = await repo.search_vehicles(
        pickup_date=pickup_date,
        return_date=return_date,
        category=category,
        transmission=transmission,
        fuel=fuel,
        min_seats=min_seats,
        max_price=max_price,
        location_id=location_id,
        sort_by=sort_by,
        featured_only=featured_only,
        skip=skip,
        limit=limit
    )
    print(f"DEBUG: repo.search_vehicles returned {len(vehicles)} vehicles")

    return VehicleDiscoveryResponse(
        total=len(vehicles),
        vehicles=vehicles,
        filters_applied={
            "category": category,
            "location_id": location_id,
            "pickup_date": pickup_date,
            "return_date": return_date,
            "sort_by": sort_by
        }
    )

@router.get("/{slug}", response_model=VehicleRead)
async def read_vehicle(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    repo = VehicleRepository(db)
    vehicle = await repo.get_by_slug(slug)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.post("/", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_in: VehicleCreate,
    db: AsyncSession = Depends(get_db)
):
    repo = VehicleRepository(db)
    return await repo.create(vehicle_in)

@router.patch("/{vehicle_id}", response_model=VehicleRead)
async def update_vehicle(
    vehicle_id: int,
    vehicle_in: VehicleUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = VehicleRepository(db)
    vehicle = await repo.update(vehicle_id, vehicle_in)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = VehicleRepository(db)
    success = await repo.delete(vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None
