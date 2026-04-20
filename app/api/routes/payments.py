from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Booking, Payment
from app.schemas.booking import PaymentBase, PaymentResponse
from app.schemas.common import BaseResponse

router = APIRouter()

@router.post("/process/", response_model=BaseResponse[PaymentResponse])
def process_payment(
    payment_in: PaymentBase,
    db: Session = Depends(get_db)
):
    db_payment = Payment(
        booking_id=payment_in.booking_id,
        amount=payment_in.amount,
        payment_method=payment_in.payment_method,
        transaction_id=payment_in.transaction_id,
        status="SUCCESS"
    )
    db.add(db_payment)
    
    booking = db.query(Booking).filter(Booking.id == payment_in.booking_id).first()
    if booking:
        booking.status = "PAYMENT_COMPLETED"
    
    db.commit()
    db.refresh(db_payment)
    
    payment_res = PaymentResponse.model_validate(db_payment)
    return BaseResponse(data=payment_res, message="Payment processed successfully")
