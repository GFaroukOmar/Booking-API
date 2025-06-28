from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

import database
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(255))

    slots = relationship("Slot", back_populates="service")
    bookings = relationship("Booking", back_populates="service")


class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_booked = Column(Boolean, default=False)

    service_id = Column(Integer, ForeignKey("services.id"))
    service = relationship("Service", back_populates="slots")

    booking = relationship("Booking", back_populates="slot", uselist=False)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    slot_id = Column(Integer, ForeignKey("slots.id"))

    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    slot = relationship("Slot", back_populates="booking")

if __name__ == '__main__':
    database.create_database()