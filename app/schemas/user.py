from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "ROLE_CUSTOMER"
    name: Optional[str] = None # Field from frontend
    phone: Optional[str] = None # Field from frontend
    workshopName: Optional[str] = None # Field from frontend for mechanics

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    
    # Parity fields for frontend
    name: Optional[str] = None
    phone: Optional[str] = None

    # Mechanic specific fields (populated if role is ROLE_MECHANIC)
    mechanicId: Optional[int] = None
    workshopName: Optional[str] = None
    specialty: Optional[str] = None
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginResponseData(BaseModel):
    token: str
    role: str

class ProfileResponse(UserResponse):
    pass # Extend later if needed
