from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Service
from schemas import ServiceCreate, ServiceUpdate, ServiceOut
from auth import admin_required


router = APIRouter(prefix="/services", tags=["Services"])

# Public: list services
@router.get("/", response_model=list[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

# Admin: create service
@router.post("/", response_model=ServiceOut)
def create_service(service: ServiceCreate, db: Session = Depends(get_db), _= Depends(admin_required)):
    existing = db.query(Service).filter(Service.name == service.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Service name already exists")
    new_service = Service(**service.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

# Admin: update service
@router.put("/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, data: ServiceUpdate, db: Session = Depends(get_db), _= Depends(admin_required)):
    service = db.query(Service).get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service

# Admin: delete service
@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db), _= Depends(admin_required)):
    service = db.query(Service).get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    return {"message": "Service deleted"}
