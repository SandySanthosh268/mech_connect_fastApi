from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Feedback, Booking, User
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=BaseResponse[FeedbackResponse])
def submit_feedback(
    feedback_in: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == feedback_in.booking_id, Booking.customer_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not owned by you")

    db_feedback = Feedback(
        booking_id=feedback_in.booking_id,
        mechanic_id=booking.mechanic_id,
        customer_id=current_user.id,
        content=feedback_in.content
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    res = FeedbackResponse.model_validate(db_feedback)
    res.customer_name = current_user.username
    return BaseResponse(data=res, message="Feedback submitted successfully")

@router.get("/mechanic/{mechanic_id}/", response_model=BaseResponse[List[FeedbackResponse]])
def get_mechanic_feedback(mechanic_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.mechanic_id == mechanic_id).order_by(Feedback.created_at.desc()).all()
    results = []
    for f in feedback:
        try:
            f_res = FeedbackResponse.model_validate(f)
            # Safe retrieval of customer name to prevent 500 crashes
            f_res.customer_name = f.customer.username if f.customer else "Verified Customer"
            results.append(f_res)
        except Exception:
            continue
    return BaseResponse(data=results)
