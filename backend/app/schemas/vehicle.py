from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class VehicleBase(BaseModel):
    slug: str
    brand: str
    model: str
    year: int
    category: str
    transmission: str
    fuel: str
    seats: int
    luggage: int
    air_conditioning: bool
    description: str
    short_description: str
    daily_price: Decimal
    status: str
    featured: bool

class VehicleCreate(VehicleBase):
    location_id: int

class VehicleUpdate(VehicleBase):
    # All fields optional for partial updates
    slug: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None
    transmission: Optional[str] = None
    fuel: Optional[str] = None
    seats: Optional[int] = None
    luggage: Optional[int] = None
    air_conditioning: Optional[bool] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    daily_price: Optional[Decimal] = None
    status: Optional[str] = None
    featured: Optional[bool] = None
    location_id: Optional[int] = None

class VehicleRead(VehicleBase):
    id: int
    location_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class VehicleReadWithImages(VehicleRead):
    images: List["VehicleImageRead"]

class VehicleDiscoveryResponse(BaseModel):
    total: int
    vehicles: List[VehicleReadWithImages]
    filters_applied: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class VehicleImageBase(BaseModel):
    url: str
    alt: Optional[str] = None
    sort_order: int = 0
    is_primary: bool = False

class VehicleImageRead(VehicleImageBase):
    id: int
    vehicle_id: int

    model_config = ConfigDict(from_attributes=True)
