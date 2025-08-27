from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Fitness Class Schemas
class FitnessClassBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    date_time: datetime = Field(..., alias="dateTime")
    instructor: str = Field(..., min_length=2, max_length=100)
    available_slots: int = Field(..., ge=1, le=100, alias="availableSlots")

class FitnessClassCreate(FitnessClassBase):
    pass

class FitnessClassResponse(FitnessClassBase):
    id: int
    total_slots: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True

# Booking Schemas
class BookingBase(BaseModel):
    class_id: int
    client_name: str = Field(..., min_length=2, max_length=100)
    client_email: EmailStr

class BookingCreate(BookingBase):
    pass

class BookingResponse(BaseModel):
    id: int
    user_id: int
    class_id: int
    client_name: str
    client_email: str
    booking_time: datetime
    fitness_class: FitnessClassResponse
    
    class Config:
        from_attributes = True