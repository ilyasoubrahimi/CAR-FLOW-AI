from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class CompanyRead(BaseModel):
    id: int
    name: str
    logo_url: Optional[str]
    primary_color: str
    secondary_color: str
    phone: str
    whatsapp_number: str
    email: str
    address: str
    default_currency: str
    timezone: str
    supported_languages: str
    booking_rules: Optional[str]
    cancellation_policy: Optional[str]
    airport_pickup_available: bool
    hotel_delivery_available: bool

    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    phone: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    default_currency: Optional[str] = None
    timezone: Optional[str] = None
    supported_languages: Optional[str] = None
    booking_rules: Optional[str] = None
    cancellation_policy: Optional[str] = None
    airport_pickup_available: Optional[bool] = None
    hotel_delivery_available: Optional[bool] = None
