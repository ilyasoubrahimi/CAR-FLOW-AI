from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.vehicle import LocationType

class LocationBase(BaseModel):
    name: str
    slug: str
    type: LocationType
    address: str
    city: str
    latitude: float
    longitude: float
    active: bool = True

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    type: Optional[LocationType] = None
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    active: Optional[bool] = None

class LocationRead(LocationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
