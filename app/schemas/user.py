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
    name: Optional[str] = None
    phone: Optional[str] = None 
    workshopName: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    is_active: bool
    
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

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
    pass 
