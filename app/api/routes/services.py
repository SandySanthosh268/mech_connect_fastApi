from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Service, MechanicProfile, User
from app.schemas.service import ServiceCreate, ServiceResponse
from app.schemas.common import BaseResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.get("/mechanic/{mechanic_id}/", response_model=BaseResponse[List[ServiceResponse]])
def get_mechanic_services(mechanic_id: int, db: Session = Depends(get_db)):
    services = db.query(Service).filter(Service.mechanic_id == mechanic_id).all()
    results = []
    for s in services:
        s_res = ServiceResponse.from_orm(s)
        s_res.mechanic_name = s.mechanic.user.username
        results.append(s_res)
    return BaseResponse(data=results)

@router.get("/my-services/", response_model=BaseResponse[List[ServiceResponse]])
def get_my_services(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    services = db.query(Service).join(MechanicProfile).filter(MechanicProfile.user_id == current_user.id).all()
    results = []
    for s in services:
        s_res = ServiceResponse.from_orm(s)
        s_res.mechanic_name = current_user.username
        results.append(s_res)
    return BaseResponse(data=results)

@router.post("/", response_model=BaseResponse[ServiceResponse])
def add_service(
    service_in: ServiceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = db.query(MechanicProfile).filter(MechanicProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=403, detail="Only mechanics can add services")
    
    db_service = Service(
        mechanic_id=profile.id,
        name=service_in.name,
        description=service_in.description,
        price=service_in.price
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    
    s_res = ServiceResponse.from_orm(db_service)
    s_res.mechanic_name = current_user.username
    return BaseResponse(data=s_res, message="Service added successfully")

@router.delete("/{id}/")
def delete_service(
    id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = db.query(Service).join(MechanicProfile).filter(
        Service.id == id,
        MechanicProfile.user_id == current_user.id
    ).first()
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found or you don't have permission")
    
    db.delete(service)
    db.commit()
    return BaseResponse(data={"message": "Deleted successfully"})
