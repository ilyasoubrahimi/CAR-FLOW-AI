from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    passport_number: str

class ReservationBase(BaseModel):
    vehicle_id: int
    pickup_datetime: datetime
    return_datetime: datetime
    extra_ids: Optional[List[int]] = []

class ReservationCreate(ReservationBase):
    customer: CustomerCreate

class ReservationRead(BaseModel):
    id: int
    reservation_code: str
    customer_id: int
    vehicle_id: int
    pickup_datetime: datetime
    return_datetime: datetime
    status: str
    total: Decimal
    currency: str

    model_config = ConfigDict(from_attributes=True)

class ReservationUpdate(BaseModel):
    pickup_datetime: Optional[datetime] = None
    return_datetime: Optional[datetime] = None
    extra_ids: Optional[List[int]] = None
