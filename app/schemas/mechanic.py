from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.user import UserResponse

class MechanicProfileBase(BaseModel):
    workshop_name: Optional[str] = None
    bio: Optional[str] = None
    specialty: Optional[str] = None
    experience_years: int = 0
    location: Optional[str] = None
    profile_picture: Optional[str] = None

class MechanicProfileCreate(MechanicProfileBase):
    pass

class MechanicProfileResponse(MechanicProfileBase):
    id: int
    user_id: int
    is_approved: bool
    user: Optional[UserResponse] = None
    
    # Calculated fields for frontend parity
    workshopName: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    name: Optional[str] = None
    average_rating: float = 0.0

    model_config = ConfigDict(from_attributes=True)
