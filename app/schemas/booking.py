from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional, List
from datetime import datetime

class BookingBase(BaseModel):
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    model_config = ConfigDict(populate_by_name=True)

    mechanic_id: int = Field(alias="mechanicId")
    service_id: int = Field(alias="serviceId")
    vehicle_id: int = Field(alias="vehicleId")
    booking_date: datetime = Field(alias="bookingDate")
    pickup_required: bool = Field(False, alias="pickupRequired")
    pickup_address: Optional[str] = Field(None, alias="pickupAddress")

class BookingResponse(BookingBase):
    id: int
    customer_id: int
    mechanic_id: int
    service_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    status: str
    scheduled_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Frontend parity fields
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    customer_address: Optional[str] = None
    mechanic_name: Optional[str] = None
    service_name: Optional[str] = None
    vehicle_info: Optional[str] = None
    amount: float = 0.0
    has_rating: bool = False
    rating_data: Optional[dict] = None
    pickup_required: bool = False

    model_config = ConfigDict(from_attributes=True)

class PickupRequestBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    booking_id: int = Field(alias="bookingId")
    pickup_location: str = Field(alias="pickupLocation")

class PickupRequestResponse(PickupRequestBase):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaymentBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # The frontend is inconsistent, sometimes sending 'booking' and sometimes 'bookingId'
    # Prioritize booking_id/bookingId for serialization (from attributes)
    booking_id: int = Field(validation_alias=AliasChoices("booking_id", "bookingId", "booking"))
    amount: float
    payment_method: str = Field(validation_alias=AliasChoices("paymentMethod", "payment_method"))
    transaction_id: str = Field(validation_alias=AliasChoices("transactionId", "transaction_id"))

class PaymentResponse(PaymentBase):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
