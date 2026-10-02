from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class ExtraRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price_type: str
    price: Decimal
    active: bool

    model_config = ConfigDict(from_attributes=True)

class ExtraCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price_type: str # PER_DAY, PER_RENTAL, FIXED
    price: Decimal
    active: bool = True

class ExtraUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_type: Optional[str] = None
    price: Optional[Decimal] = None
    active: Optional[bool] = None
