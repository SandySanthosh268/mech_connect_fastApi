from sqlalchemy import Boolean, Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    
    full_name = Column(String(255), nullable=True)
    
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="ROLE_CUSTOMER")
    phone_number = Column(String(15), nullable=True)
    address = Column(Text, nullable=True)
    
    mechanic_profile = relationship("MechanicProfile", back_populates="user", uselist=False)
    vehicles = relationship("Vehicle", back_populates="owner")
    bookings = relationship("Booking", foreign_keys="[Booking.customer_id]", back_populates="customer")

class MechanicProfile(Base):
    __tablename__ = "api_mechanicprofile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), unique=True)
    workshop_name = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    specialty = Column(String(255), nullable=True)
    experience_years = Column(Integer, default=0)
    is_approved = Column(Boolean, default=False)
    location = Column(String(255), nullable=True)

    user = relationship("User", back_populates="mechanic_profile")
    services = relationship("Service", back_populates="mechanic")
    bookings = relationship("Booking", foreign_keys="[Booking.mechanic_id]", back_populates="mechanic")
    ratings = relationship("Rating", back_populates="mechanic")
    feedbacks = relationship("Feedback", back_populates="mechanic")

class Service(Base):
    __tablename__ = "api_service"

    id = Column(Integer, primary_key=True, index=True)
    mechanic_id = Column(Integer, ForeignKey("api_mechanicprofile.id"))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False) # Changed from decimal to float for generic use, though numeric is better for exact currency

    mechanic = relationship("MechanicProfile", back_populates="services")

class Vehicle(Base):
    __tablename__ = "api_vehicle"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users_user.id"))
    type = Column(String(10), default="CAR")
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    registration_number = Column(String(20), unique=True, nullable=False)
    owner = relationship("User", back_populates="vehicles")

class Booking(Base):
    __tablename__ = "api_booking"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users_user.id"))
    mechanic_id = Column(Integer, ForeignKey("api_mechanicprofile.id"))
    service_id = Column(Integer, ForeignKey("api_service.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("api_vehicle.id"), nullable=True)
    
    status = Column(String(30), default="REQUESTED")
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text, nullable=True)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="bookings")
    mechanic = relationship("MechanicProfile", foreign_keys=[mechanic_id], back_populates="bookings")
    service = relationship("Service")
    vehicle = relationship("Vehicle")
    
    rating = relationship("Rating", back_populates="booking", uselist=False)
    feedback = relationship("Feedback", back_populates="booking", uselist=False)
    pickup_request = relationship("PickupRequest", back_populates="booking", uselist=False)
    payment = relationship("Payment", back_populates="booking", uselist=False)

class Rating(Base):
    __tablename__ = "api_rating"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("api_booking.id"), unique=True)
    mechanic_id = Column(Integer, ForeignKey("api_mechanicprofile.id"))
    customer_id = Column(Integer, ForeignKey("users_user.id"))
    score = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="rating")
    mechanic = relationship("MechanicProfile", back_populates="ratings")
    customer = relationship("User")

class Feedback(Base):
    __tablename__ = "api_feedback"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("api_booking.id"), unique=True)
    mechanic_id = Column(Integer, ForeignKey("api_mechanicprofile.id"))
    customer_id = Column(Integer, ForeignKey("users_user.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="feedback")
    mechanic = relationship("MechanicProfile", back_populates="feedbacks")
    customer = relationship("User")

class PickupRequest(Base):
    __tablename__ = "api_pickuprequest"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("api_booking.id"), unique=True)
    pickup_location = Column(Text, nullable=False)
    status = Column(String(20), default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="pickup_request")

class Payment(Base):
    __tablename__ = "api_payment"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("api_booking.id"), unique=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(20), default="UPI")
    transaction_id = Column(String(255), unique=True, nullable=False)
    status = Column(String(20), default="SUCCESS")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="payment")
