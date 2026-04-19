from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Rating, Booking, User
from app.schemas.feedback import RatingCreate, RatingResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=BaseResponse[RatingResponse])
def submit_rating(
    rating_in: RatingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if booking exists and belongs to user
    booking = db.query(Booking).filter(Booking.id == rating_in.booking_id, Booking.customer_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not owned by you")
        
    # Check if already rated
    existing = db.query(Rating).filter(Rating.booking_id == rating_in.booking_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already rated this booking.")
        
    if booking.status not in ('COMPLETED', 'PAYMENT_COMPLETED'):
        raise HTTPException(status_code=400, detail="You can only rate completed bookings.")

    db_rating = Rating(
        booking_id=rating_in.booking_id,
        mechanic_id=booking.mechanic_id,
        customer_id=current_user.id,
        score=rating_in.score,
        comment=rating_in.comment
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    res = RatingResponse.model_validate(db_rating)
    res.customer_name = current_user.username
    return BaseResponse(data=res, message="Rating submitted successfully")

@router.get("/check/{booking_id}/")
def check_booking_rating(booking_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.booking_id == booking_id).first()
    has_rating = rating is not None
    rating_data = None
    if has_rating:
        rating_data = {
            "id": rating.id,
            "score": rating.score,
            "comment": rating.comment,
            "created_at": rating.created_at
        }
    return BaseResponse(data={"has_rating": has_rating, "rating": rating_data})

@router.get("/mechanic/{mechanic_id}/", response_model=BaseResponse[List[RatingResponse]])
def get_mechanic_ratings(mechanic_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.mechanic_id == mechanic_id).order_by(Rating.created_at.desc()).all()
    results = []
    for r in ratings:
        try:
            r_res = RatingResponse.model_validate(r)
            # Safe retrieval of customer name to prevent 500 crashes
            r_res.customer_name = r.customer.username if r.customer else "Verified Customer"
            results.append(r_res)
        except Exception:
            continue
    return BaseResponse(data=results)
