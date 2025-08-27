from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking, FitnessClass, User
from app.schemas import BookingCreate, BookingResponse
from app.dependencies import get_current_user
from datetime import datetime
import pytz

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def book_class(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if class exists
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == booking.class_id).first()
    if not fitness_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Check if class is in future
    current_time = datetime.now(IST)
    if fitness_class.date_time <= current_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book past classes"
        )
    
    # Check if slots available
    if fitness_class.available_slots <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available slots for this class"
        )
    
    # Check if user already booked this class
    existing_booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.class_id == booking.class_id
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this class"
        )
    
    # Create booking
    db_booking = Booking(
        user_id=current_user.id,
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email
    )
    
    # Reduce available slots
    fitness_class.available_slots -= 1
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    return {
        "message": "Class booked successfully",
        "booking_id": db_booking.id,
        "class_name": fitness_class.name,
        "remaining_slots": fitness_class.available_slots
    }

@router.get("/", response_model=List[BookingResponse])
def get_user_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.booking_time.desc()).all()
    
    return bookings

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check if class is in future
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == booking.class_id).first()
    current_time = datetime.now(IST)
    
    if fitness_class.date_time <= current_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel booking for past classes"
        )
    
    # Increase available slots
    fitness_class.available_slots += 1
    
    db.delete(booking)
    db.commit()
    
    return {"message": "Booking cancelled successfully"}