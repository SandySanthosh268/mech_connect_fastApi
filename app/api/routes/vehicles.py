from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Vehicle, User
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=BaseResponse[List[VehicleResponse]])
def get_my_vehicles(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    vehicles = db.query(Vehicle).filter(Vehicle.owner_id == current_user.id).all()
    return BaseResponse(data=vehicles)

@router.post("/", response_model=BaseResponse[VehicleResponse])
def add_vehicle(
    vehicle_in: VehicleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    reg_no = vehicle_in.registration_number or vehicle_in.registrationNumber
    if not reg_no:
        raise HTTPException(status_code=400, detail="Registration number is required")
        
    db_vehicle = Vehicle(
        owner_id=current_user.id,
        type=vehicle_in.type,
        brand=vehicle_in.brand,
        model=vehicle_in.model,
        registration_number=reg_no
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return BaseResponse(data=db_vehicle, message="Vehicle added successfully")

@router.delete("/{id}/")
def delete_vehicle(
    id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == id,
        Vehicle.owner_id == current_user.id
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return BaseResponse(data={"message": "Deleted successfully"})
