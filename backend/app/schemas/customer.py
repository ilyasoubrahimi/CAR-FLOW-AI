from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    country: Optional[str] = None
    preferred_language: str = "fr"

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
