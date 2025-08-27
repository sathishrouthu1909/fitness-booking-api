from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="user")
    created_classes = relationship("FitnessClass", back_populates="creator")

class FitnessClass(Base):
    __tablename__ = "fitness_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_time = Column(DateTime(timezone=True), nullable=False)
    instructor = Column(String, nullable=False)
    available_slots = Column(Integer, nullable=False)
    total_slots = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_classes")
    bookings = relationship("Booking", back_populates="fitness_class")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer, ForeignKey("fitness_classes.id"))
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    booking_time = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    fitness_class = relationship("FitnessClass", back_populates="bookings")