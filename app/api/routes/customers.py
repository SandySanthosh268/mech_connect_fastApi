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
    # Update User fields
    if "first_name" in profile_data: current_user.first_name = profile_data["first_name"]
    if "last_name" in profile_data: current_user.last_name = profile_data["last_name"]
    if "name" in profile_data: 
        # Optionally split name or just store in first_name
        current_user.first_name = profile_data["name"]
    if "email" in profile_data: current_user.email = profile_data["email"]
    if "phone_number" in profile_data: current_user.phone_number = profile_data["phone_number"]
    if "phone" in profile_data: current_user.phone_number = profile_data["phone"]
    if "address" in profile_data: current_user.address = profile_data["address"]
    
    db.commit()
    db.refresh(current_user)
    
    res = UserResponse.from_orm(current_user)
    res.name = f"{current_user.first_name} {current_user.last_name or ''}".strip() or current_user.username
    res.phone = current_user.phone_number
    
    return BaseResponse(data=res, message="Profile updated successfully")
