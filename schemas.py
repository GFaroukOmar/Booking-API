from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str


class BookingCreate(BaseModel):
    service_id: int
    slot_id: int

class BookingOut(BaseModel):
    id: int
    service_id: int
    slot_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class SlotOut(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    is_booked: bool

    class Config:
        orm_mode = True

class ServiceOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class SlotCreate(BaseModel):
    service_id: int
    start_time: datetime
    end_time: datetime

class SlotUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_booked: Optional[bool] = None
