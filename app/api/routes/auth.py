from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse, LoginResponseData
from app.schemas.common import BaseResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel

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
    
    if user.role == "ROLE_MECHANIC":
        profile = db.query(MechanicProfile).filter(MechanicProfile.user_id == user.id).first()
        if not profile or not profile.is_approved:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your mechanic account is pending admin approval. Please try again once approved."
            )
    
    access_token = create_access_token(subject=str(user.id))
    return BaseResponse(
        data=LoginResponseData(token=access_token, role=user.role),
        message="Login successful"
    )

from app.db.models import User, MechanicProfile

@router.post("/register/", response_model=BaseResponse[UserResponse])
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_by_email = db.query(User).filter(User.email == user_in.email).first()
    if user_by_email:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    
    username = user_in.username or user_in.email
    user_by_username = db.query(User).filter(User.username == username).first()
    if user_by_username:

        username = f"{user_in.email}_{func.now()}" # Fallback
    
    full_name = user_in.name or user_in.first_name or user_in.username
    phone_number = user_in.phone or user_in.phone_number
    
    user_db = User(
        email=user_in.email,
        username=username,
        password=get_password_hash(user_in.password),
        full_name=full_name,
        phone_number=phone_number,
        address=user_in.address,
        role=user_in.role or "ROLE_CUSTOMER"
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    
    if user_db.role == "ROLE_MECHANIC":
        profile = MechanicProfile(
            user_id=user_db.id,
            workshop_name=user_in.workshopName,
            is_approved=False 
        )
        db.add(profile)
        db.commit()
    
    message = "User registered successfully"
    if user_db.role == "ROLE_MECHANIC":
        message = "Registration successful. Your account is pending admin approval. You will be able to log in once verified."
    
    return BaseResponse(data=user_db, message=message)
