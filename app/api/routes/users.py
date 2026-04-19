from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import ProfileResponse, UserResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

from app.db.models import User, MechanicProfile

@router.get("/me/", response_model=BaseResponse[UserResponse])
def get_user_me(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    res = UserResponse.from_orm(current_user)
    res.name = f"{current_user.first_name} {current_user.last_name or ''}".strip() or current_user.username
    res.phone = current_user.phone_number
    
    if current_user.role == "ROLE_MECHANIC":
        profile = db.query(MechanicProfile).filter(MechanicProfile.user_id == current_user.id).first()
        if profile:
            res.mechanicId = profile.id
            res.workshopName = profile.workshop_name
            res.specialty = profile.specialty
            res.experience_years = profile.experience_years
            res.bio = profile.bio
            res.location = profile.location
            
    return BaseResponse(data=res, message="Profile retrieved successfully")
