from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.database import get_db
from app.db.models import User, MechanicProfile, Booking
from app.schemas.mechanic import MechanicProfileResponse
from app.schemas.user import UserResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user
from app.api.routes.mechanics import get_mechanic_extra_info

router = APIRouter()

def is_admin(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "ROLE_ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/customers/", response_model=BaseResponse[List[UserResponse]])
def admin_customers(db: Session = Depends(get_db), _ = Depends(is_admin)):
    customers = db.query(User).filter(User.role == "ROLE_CUSTOMER").all()
    results = []
    for c in customers:
        res = UserResponse.model_validate(c)
        res.name = c.full_name or c.username
        res.phone = c.phone_number
        results.append(res)
    return BaseResponse(data=results)

@router.get("/mechanics/", response_model=BaseResponse[List[MechanicProfileResponse]])
def admin_mechanics(db: Session = Depends(get_db), _ = Depends(is_admin)):
    mechanics = db.query(MechanicProfile).all()
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

@router.get("/mechanics/pending/", response_model=BaseResponse[List[MechanicProfileResponse]])
def admin_pending_mechanics(db: Session = Depends(get_db), _ = Depends(is_admin)):
    mechanics = db.query(MechanicProfile).filter(MechanicProfile.is_approved == False).all()
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

@router.patch("/mechanics/{id}/approve/")
def approve_mechanic(id: int, db: Session = Depends(get_db), _ = Depends(is_admin)):
    profile = db.query(MechanicProfile).filter(MechanicProfile.id == id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    profile.is_approved = True
    db.commit()
    return BaseResponse(data={"message": "Mechanic approved successfully"})

@router.patch("/mechanics/{id}/reject/")
def reject_mechanic(id: int, db: Session = Depends(get_db), _ = Depends(is_admin)):
    profile = db.query(MechanicProfile).filter(MechanicProfile.id == id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    profile.is_approved = False # In original Django it just set is_approved to False
    db.commit()
    return BaseResponse(data={"message": "Mechanic rejected successfully"})

@router.get("/dashboard/stats/")
def get_admin_stats(db: Session = Depends(get_db), _ = Depends(is_admin)):
    total_customers = db.query(User).filter(User.role == "ROLE_CUSTOMER").count()
    total_mechanics = db.query(User).filter(User.role == "ROLE_MECHANIC").count()
    total_bookings = db.query(Booking).count()
    pending_bookings = db.query(Booking).filter(Booking.status == "PENDING").count()
    completed_bookings = db.query(Booking).filter(Booking.status == "COMPLETED").count()
    pending_approvals = db.query(MechanicProfile).filter(MechanicProfile.is_approved == False).count()
    
    return BaseResponse(data={
        "totalCustomers": total_customers,
        "totalMechanics": total_mechanics,
        "totalBookings": total_bookings,
        "pendingBookings": pending_bookings,
        "completedBookings": completed_bookings,
        "pendingApprovals": pending_approvals,
    })
