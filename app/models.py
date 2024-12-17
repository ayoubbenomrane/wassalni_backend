from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean,Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    firstName = Column(String(255), nullable=False, index=True)
    lastName = Column(String(255), nullable=False, index=True)
    phoneNumber = Column(String(20), nullable=True)
    profilePicture = Column(Text, nullable=True)
    gender = Column(String(255), nullable=True)
    birthDay = Column(Date, nullable=True)  # Added birthDay column
    password = Column(String(255), nullable=False)
    rating=Column(Float,default=5)
    email = Column(String(255), index=True, nullable=False)
    carpools = relationship("Carpool", back_populates="owner")
    bookings = relationship("Booking", back_populates="user")
    feedback_received = relationship("Feedback", back_populates="receiver", foreign_keys="Feedback.receiver_id")
    feedback_given = relationship("Feedback", back_populates="giver", foreign_keys="Feedback.giver_id")
    
# Carpool Model
class Carpool(Base):
    __tablename__ = "carpools"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    departure = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    seats_available = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Updated to reference "users.id"

    owner = relationship("User", back_populates="carpools")
    bookings = relationship("Booking", back_populates="carpool")


# Booking Model
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Reference to "users.id"
    carpool_id = Column(Integer, ForeignKey("carpools.id"), nullable=False)
    seats_booked = Column(Integer, nullable=False)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    carpool = relationship("Carpool", back_populates="bookings")


# Feedback Model
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Reference to "users.id"
    giver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    receiver = relationship("User", back_populates="feedback_received", foreign_keys=[receiver_id])
    giver = relationship("User", back_populates="feedback_given", foreign_keys=[giver_id])
