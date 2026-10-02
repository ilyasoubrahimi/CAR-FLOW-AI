from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

class AvailabilityRequest(BaseModel):
    vehicle_id: int
    pickup_datetime: datetime
    return_datetime: datetime

class AvailabilityResponse(BaseModel):
    available: bool
    message: Optional[str] = None

class QuoteRequest(BaseModel):
    vehicle_id: int
    pickup_datetime: datetime
    return_datetime: datetime
    extra_ids: Optional[List[int]] = []

class QuoteResponse(BaseModel):
    subtotal: Decimal
    discount: Decimal
    extras_total: Decimal
    delivery_fee: Decimal
    total: Decimal
    currency: str
    pricing_breakdown: dict
