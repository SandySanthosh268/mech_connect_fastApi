from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.put("/profile/", response_model=BaseResponse[UserResponse])
def update_customer_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if "full_name" in profile_data: current_user.full_name = profile_data["full_name"]
    if "name" in profile_data: current_user.full_name = profile_data["name"]
    if "email" in profile_data: current_user.email = profile_data["email"]
    if "phone_number" in profile_data: current_user.phone_number = profile_data["phone_number"]
    if "phone" in profile_data: current_user.phone_number = profile_data["phone"]
    if "address" in profile_data: current_user.address = profile_data["address"]
    
    db.commit()
    db.refresh(current_user)
    
    res = UserResponse.model_validate(current_user)
    res.name = current_user.full_name or current_user.username
    res.phone = current_user.phone_number
    
    return BaseResponse(data=res, message="Profile updated successfully")
