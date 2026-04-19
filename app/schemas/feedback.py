from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from datetime import datetime

class RatingBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    booking_id: int = Field(validation_alias=AliasChoices("booking_id", "bookingId", "booking"))
    score: int
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    mechanic_id: int
    customer_id: int
    customer_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FeedbackBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    booking_id: int = Field(validation_alias=AliasChoices("booking_id", "bookingId", "booking"))
    content: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    mechanic_id: int
    customer_id: int
    customer_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
