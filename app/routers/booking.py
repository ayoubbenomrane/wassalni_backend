from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Booking, Carpool
from app.database import get_db
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse, BookingListResponse
from app.utils import get_current_user

# Initialize the router
router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


# Create a new booking
@router.post("", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a new booking for a carpool.
    """
    # Check if the carpool exists
    carpool = db.query(Carpool).filter(Carpool.id == booking.carpool_id).first()
    if not carpool:
        raise HTTPException(status_code=404, detail="Carpool not found")
    
    # Check if enough seats are available
    if booking.seats_booked > carpool.seats_available:
        raise HTTPException(status_code=400, detail="Not enough seats available")

    # Create the booking
    new_booking = Booking(
        carpool_id=booking.carpool_id,
        user_id=current_user.id,
        seats_booked=booking.seats_booked,
        is_confirmed=False,  # Default state is unconfirmed
    )

    # Update available seats in the carpool
    carpool.seats_available -= booking.seats_booked

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# Retrieve all bookings for the current user
@router.get("", response_model=BookingListResponse)
def get_user_bookings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Retrieve all bookings made by the current user.
    """
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return {"bookings": bookings}


# Confirm or Update a Booking
@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update the status of a booking (e.g., confirm it).
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Ensure only the owner of the carpool can confirm the booking
    carpool = db.query(Carpool).filter(Carpool.id == booking.carpool_id).first()
    if not carpool or carpool.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to confirm this booking")

    # Update fields dynamically
    for key, value in booking_update.dict(exclude_unset=True).items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking


# Delete a booking
@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a booking.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Ensure only the user who made the booking can delete it
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this booking")

    # Restore the seats in the carpool
    carpool = db.query(Carpool).filter(Carpool.id == booking.carpool_id).first()
    if carpool:
        carpool.seats_available += booking.seats_booked

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
