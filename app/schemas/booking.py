from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Base Booking Schema
class BookingBase(BaseModel):
    carpool_id: int
    seats_booked: int


# Schema for Creating a Booking
class BookingCreate(BookingBase):
    """
    Schema for creating a new booking.
    """
    pass


# Schema for Updating a Booking
class BookingUpdate(BaseModel):
    """
    Schema for updating booking details.
    """
    is_confirmed: Optional[bool] = None


# Schema for Booking Response
class BookingResponse(BookingBase):
    """
    Schema for returning booking details in responses.
    """
    id: int
    user_id: int
    is_confirmed: bool
    created_at: datetime

    class Config:
        orm_mode = True


# Schema for a List of Bookings
class BookingListResponse(BaseModel):
    """
    Schema for returning multiple bookings.
    """
    bookings: List[BookingResponse]

    class Config:
        orm_mode = True
