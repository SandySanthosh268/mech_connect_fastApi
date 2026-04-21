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

from pydantic import BaseModel, EmailStr, ConfigDict, model_validator, field_validator
import re

class UserCreate(UserBase):
    password: str
    confirm_password: str
    role: Optional[str] = "ROLE_CUSTOMER"
    name: Optional[str] = None
    phone: Optional[str] = None 
    workshopName: Optional[str] = None

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[@#$%^&+=!]', v):
            raise ValueError('Password must contain at least one special character (@#$%^&+=!)')
        return v

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreate':
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self

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
