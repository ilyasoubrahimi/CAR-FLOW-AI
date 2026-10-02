from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
