from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Booking, PickupRequest, User
from app.schemas.booking import PickupRequestResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("/request/", response_model=BaseResponse[PickupRequestResponse])
def request_pickup(
    pickup_in: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    booking_id = pickup_in.get("booking")
    location = pickup_in.get("pickup_location")
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    db_pickup = PickupRequest(
        booking_id=booking_id,
        pickup_location=location,
        status="PENDING"
    )
    db.add(db_pickup)
    db.commit()
    db.refresh(db_pickup)
    return BaseResponse(data=db_pickup)

@router.patch("/{id}/status/", response_model=BaseResponse[PickupRequestResponse])
def update_pickup_status(
    id: int,
    status_update: dict,
    db: Session = Depends(get_db)
):
    pickup = db.query(PickupRequest).filter(PickupRequest.id == id).first()
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup request not found")
    
    new_status = status_update.get("status")
    if new_status:
        pickup.status = new_status
        db.commit()
        db.refresh(pickup)
    return BaseResponse(data=pickup)
