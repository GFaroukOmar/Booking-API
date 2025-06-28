from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Slot
from schemas import SlotCreate, SlotUpdate, SlotOut
from auth import  admin_required

router = APIRouter(prefix="/slots", tags=["Slots"])

# Public: list all available slots
@router.get("/", response_model=list[SlotOut])
def list_slots(db: Session = Depends(get_db)):
    return db.query(Slot).filter(Slot.is_booked == False).all()

# Admin: create slot
@router.post("/", response_model=SlotOut)
def create_slot(slot: SlotCreate, db: Session = Depends(get_db), _= Depends(admin_required)):
    new_slot = Slot(**slot.dict())
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot

# Admin: update slot
@router.put("/{slot_id}", response_model=SlotOut)
def update_slot(slot_id: int, data: SlotUpdate, db: Session = Depends(get_db), _= Depends(admin_required)):
    slot = db.query(Slot).get(slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(slot, field, value)
    db.commit()
    db.refresh(slot)
    return slot

# Admin: delete slot
@router.delete("/{slot_id}")
def delete_slot(slot_id: int, db: Session = Depends(get_db), _= Depends(admin_required)):
    slot = db.query(Slot).get(slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    db.delete(slot)
    db.commit()
    return {"message": "Slot deleted"}
