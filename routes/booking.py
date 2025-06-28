from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Booking, Slot
from schemas import BookingCreate, BookingOut
from auth import get_current_user, admin_required

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# Create a booking
@router.post("/", response_model=BookingOut)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    slot = db.query(Slot).filter(Slot.id == data.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    if slot.is_booked:
        raise HTTPException(status_code=400, detail="Slot already booked")
    booking = Booking(
        user_id=current_user.id,
        service_id=data.service_id,
        slot_id=data.slot_id,
        status="confirmed"
    )
    slot.is_booked = True
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

# View my bookings
@router.get("/", response_model=list[BookingOut])
def list_user_bookings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()

# Cancel a booking
@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    slot = db.query(Slot).get(booking.slot_id)
    if slot:
        slot.is_booked = False
    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled"}


@router.get("/all", response_model=list[BookingOut])
def all_bookings(db: Session = Depends(get_db), _=Depends(admin_required)):
    return db.query(Booking).all()