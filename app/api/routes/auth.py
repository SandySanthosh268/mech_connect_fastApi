from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse, LoginResponseData
from app.schemas.common import BaseResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login/", response_model=BaseResponse[LoginResponseData])
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(subject=str(user.id))
    return BaseResponse(
        data=LoginResponseData(token=access_token, role=user.role),
        message="Login successful"
    )

from app.db.models import User, MechanicProfile

@router.post("/register/", response_model=BaseResponse[UserResponse])
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if existing user by email
    user_by_email = db.query(User).filter(User.email == user_in.email).first()
    if user_by_email:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Handle username parity (Djangos requirement)
    username = user_in.username or user_in.email
    user_by_username = db.query(User).filter(User.username == username).first()
    if user_by_username:
        # If email is unique but username (e.g. email) is taken, something is weird
        # or it's just a collision on username.
        username = f"{user_in.email}_{func.now()}" # Fallback
    
    # Map frontend fields
    first_name = user_in.first_name or user_in.name
    phone_number = user_in.phone_number or user_in.phone
    
    user_db = User(
        email=user_in.email,
        username=username,
        password=get_password_hash(user_in.password),
        first_name=first_name,
        last_name=user_in.last_name,
        phone_number=phone_number,
        address=user_in.address,
        role=user_in.role or "ROLE_CUSTOMER"
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    # Automatic Profile Creation for Mechanics
    if user_db.role == "ROLE_MECHANIC":
        profile = MechanicProfile(
            user_id=user_db.id,
            workshop_name=user_in.workshopName,
            is_approved=False # Admin must approve
        )
        db.add(profile)
        db.commit()
    
    return BaseResponse(data=user_db, message="User registered successfully")
