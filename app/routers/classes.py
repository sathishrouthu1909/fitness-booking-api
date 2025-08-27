from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FitnessClass, User
from app.schemas import FitnessClassCreate, FitnessClassResponse
from app.dependencies import get_current_user
import pytz

router = APIRouter(prefix="/classes", tags=["Classes"])

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

@router.post("/", response_model=FitnessClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    fitness_class: FitnessClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Convert datetime to IST
    class_datetime = fitness_class.date_time
    if class_datetime.tzinfo is None:
        class_datetime = IST.localize(class_datetime)
    else:
        class_datetime = class_datetime.astimezone(IST)
    
    # Validate future datetime
    if class_datetime <= datetime.now(IST):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class datetime must be in the future"
        )
    
    db_class = FitnessClass(
        name=fitness_class.name,
        date_time=class_datetime,
        instructor=fitness_class.instructor,
        available_slots=fitness_class.available_slots,
        total_slots=fitness_class.available_slots,
        created_by=current_user.id
    )
    
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    
    return db_class

@router.get("/", response_model=List[FitnessClassResponse])
def get_classes(db: Session = Depends(get_db)):
    # Get upcoming classes only
    current_time = datetime.now(IST)
    classes = db.query(FitnessClass).filter(
        FitnessClass.date_time > current_time
    ).order_by(FitnessClass.date_time).all()
    
    return classes

@router.get("/{class_id}", response_model=FitnessClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db)):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
    
    if not fitness_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    return fitness_class