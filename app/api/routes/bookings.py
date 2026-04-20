from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Booking, PickupRequest, Payment, User, MechanicProfile, Service, Vehicle, Rating
from app.schemas.booking import BookingCreate, BookingResponse, PickupRequestResponse, PaymentBase, PaymentResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user
from datetime import datetime

router = APIRouter()

def get_booking_response(booking: Booking, db: Session):
    customer = booking.customer
    mechanic_user = booking.mechanic.user
    
    res = BookingResponse.model_validate(booking)
    res.customer_name = customer.username
    res.customer_phone = customer.phone_number
    res.customer_email = customer.email
    res.customer_address = customer.address
    res.mechanic_name = mechanic_user.username
    res.service_name = booking.service.name if booking.service else None
    
    if booking.vehicle:
        res.vehicle_info = f"{booking.vehicle.type} {booking.vehicle.brand} {booking.vehicle.model}"
    
    if booking.payment:
        res.amount = booking.payment.amount
    elif booking.service:
        res.amount = booking.service.price
    else:
        res.amount = 0.0

    res.has_rating = booking.rating is not None
    if booking.rating:
        res.rating_data = {
            "id": booking.rating.id,
            "score": booking.rating.score,
            "comment": booking.rating.comment,
            "customer_name": customer.username,
            "created_at": booking.rating.created_at
        }
    
    res.pickup_required = booking.pickup_request is not None
    
    return res

@router.post("/", response_model=BaseResponse[BookingResponse])
def create_booking(
    booking_in: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_booking = Booking(
        customer_id=current_user.id,
        mechanic_id=booking_in.mechanic_id,
        service_id=booking_in.service_id,
        vehicle_id=booking_in.vehicle_id,
        scheduled_at=booking_in.booking_date,
        notes=booking_in.notes,
        status="REQUESTED"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    if booking_in.pickup_required and booking_in.pickup_address:
        db_pickup = PickupRequest(
            booking_id=db_booking.id,
            pickup_location=booking_in.pickup_address,
            status="PENDING"
        )
        db.add(db_pickup)
        db.commit()
    
    return BaseResponse(data=get_booking_response(db_booking, db), message="Booking created successfully")

@router.get("/customer/", response_model=BaseResponse[List[BookingResponse]])
def get_customer_bookings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).filter(Booking.customer_id == current_user.id).order_by(Booking.created_at.desc()).all()
    results = [get_booking_response(b, db) for b in bookings]
    return BaseResponse(data=results)

@router.get("/mechanic/", response_model=BaseResponse[List[BookingResponse]])
def get_mechanic_bookings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).join(MechanicProfile).filter(MechanicProfile.user_id == current_user.id).order_by(Booking.created_at.desc()).all()
    results = [get_booking_response(b, db) for b in bookings]
    return BaseResponse(data=results)

@router.patch("/{id}/status/", response_model=BaseResponse[BookingResponse])
def update_booking_status(
    id: int,
    status_update: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    new_status = status_update.get("status")
    if new_status:
        booking.status = new_status
        db.commit()
        db.refresh(booking)
    
    return BaseResponse(data=get_booking_response(booking, db))

