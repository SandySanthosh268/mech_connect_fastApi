from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from app.db.database import get_db
from app.db.models import MechanicProfile, User, Rating
from app.schemas.mechanic import MechanicProfileResponse
from app.schemas.user import UserResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

def get_mechanic_extra_info(mechanic: MechanicProfile, db: Session):
    avg_rating = db.query(func.avg(Rating.score)).filter(Rating.mechanic_id == mechanic.id).scalar() or 0.0
    
    
    user = mechanic.user
    name = user.full_name or user.username
    
    return {
        "workshopName": mechanic.workshop_name or (f"{name}'s Workshop" if name else "Workshop"),
        "phone": user.phone_number,
        "address": user.address,
        "name": name,
        "average_rating": float(avg_rating)
    }

@router.get("/approved/", response_model=BaseResponse[List[MechanicProfileResponse]])
def get_approved_mechanics(db: Session = Depends(get_db)):
    mechanics = db.query(MechanicProfile).filter(MechanicProfile.is_approved == True).all()
    results = []
    for m in mechanics:
        extra = get_mechanic_extra_info(m, db)
    
        m_res = MechanicProfileResponse.model_validate(m)
        m_res.workshopName = extra["workshopName"]
        m_res.phone = extra["phone"]
        m_res.address = extra["address"]
        m_res.name = extra["name"]
        m_res.average_rating = extra["average_rating"]
        results.append(m_res)
    return BaseResponse(data=results)

@router.get("/search/", response_model=BaseResponse[List[MechanicProfileResponse]])
def search_mechanics(query: Optional[str] = Query(""), db: Session = Depends(get_db)):
    db_query = db.query(MechanicProfile).join(User).filter(MechanicProfile.is_approved == True)
    
    if query:
        db_query = db_query.filter(
            or_(
                User.username.icontains(query),
                User.full_name.icontains(query),
                MechanicProfile.specialty.icontains(query),
                MechanicProfile.location.icontains(query)
            )
        )
    
    mechanics = db_query.all()
    results = []
    for m in mechanics:
        extra = get_mechanic_extra_info(m, db)
        m_res = MechanicProfileResponse.model_validate(m)
        m_res.workshopName = extra["workshopName"]
        m_res.phone = extra["phone"]
        m_res.address = extra["address"]
        m_res.name = extra["name"]
        m_res.average_rating = extra["average_rating"]
        results.append(m_res)
    return BaseResponse(data=results)

@router.put("/profile/", response_model=BaseResponse[MechanicProfileResponse])
def update_mechanic_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = db.query(MechanicProfile).filter(MechanicProfile.user_id == current_user.id).first()
    if not profile:
        profile = MechanicProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    if "full_name" in profile_data: current_user.full_name = profile_data["full_name"]
    if "name" in profile_data: current_user.full_name = profile_data["name"]
    if "email" in profile_data: current_user.email = profile_data["email"]
    if "phone_number" in profile_data: current_user.phone_number = profile_data["phone_number"]
    if "phone" in profile_data: current_user.phone_number = profile_data["phone"]
    if "address" in profile_data: current_user.address = profile_data["address"]
    
    
    if "workshop_name" in profile_data: profile.workshop_name = profile_data["workshop_name"]
    if "workshopName" in profile_data: profile.workshop_name = profile_data["workshopName"]
    if "bio" in profile_data: profile.bio = profile_data["bio"]
    if "specialty" in profile_data: profile.specialty = profile_data["specialty"]
    if "experience_years" in profile_data: profile.experience_years = profile_data["experience_years"]
    if "location" in profile_data: profile.location = profile_data["location"]
    if "profile_picture" in profile_data: profile.profile_picture = profile_data["profile_picture"]
    
    db.commit()
    db.refresh(profile)
    db.refresh(current_user)
    
    extra = get_mechanic_extra_info(profile, db)
    m_res = MechanicProfileResponse.model_validate(profile)
    m_res.workshopName = extra["workshopName"]
    m_res.phone = extra["phone"]
    m_res.address = extra["address"]
    m_res.name = extra["name"]
    m_res.average_rating = extra["average_rating"]
    
    return BaseResponse(data=m_res, message="Profile updated successfully")
