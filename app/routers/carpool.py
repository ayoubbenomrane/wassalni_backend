from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.models import Carpool
from app.database import get_db
from app.schemas.carpool import CarpoolCreate, CarpoolUpdate, CarpoolResponse, CarpoolListResponse
from app.oauth2 import get_current_user

# Initialize the router
router = APIRouter(
    tags=["Carpools"]
)


# Create a new carpool
@router.post("", response_model=CarpoolResponse)
def create_carpool(
    carpool: CarpoolCreate,
    db: Session = Depends(get_db),
    current_user:int =Depends(get_current_user),
):
    """
    Create a new carpool entry.
    """
    new_carpool = Carpool(
        price=carpool.price,
        departure=carpool.departure,
        destination=carpool.destination,
        time=carpool.time,
        seats_available=carpool.seats_available,
        owner_id=current_user.id,  # Owner is the current authenticated user
    )
    db.add(new_carpool)
    db.commit()
    db.refresh(new_carpool)
    return new_carpool


# Retrieve all carpools
@router.get("", response_model=CarpoolListResponse)



# Retrieve all carpools with optional query selectors
@router.get("/", response_model=CarpoolListResponse)
def get_all_carpools(
    db: Session = Depends(get_db),
    destination: str = Query(None, description="Destination city"),
    departure: str = Query(None, description="Source city"),
    date: str = Query(None, description="Departure date (YYYY-MM-DD)"),
    min_seats: int = Query(None, description="Minimum number of available seats")
):
  
    # Start with the base query
    query = db.query(Carpool)

    # Apply filters if query parameters are provided
    if destination:
        query = query.filter(Carpool.destination == destination)
    if departure:
        query = query.filter(Carpool.departure == departure)
    if date:
        try:
            # Parse the date string and filter only by date
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(cast(Carpool.time, Date) == date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'")

    if min_seats is not None:
        query = query.filter(Carpool.seats_available >= min_seats)

    # Execute the query
    carpools = query.all()
    return {"carpools": carpools}

# Retrieve a single carpool by ID
@router.get("/{carpool_id}", response_model=CarpoolResponse)
def get_carpool(carpool_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a carpool by its ID.
    """
    carpool = db.query(Carpool).filter(Carpool.id == carpool_id).first()
    if not carpool:
        raise HTTPException(status_code=404, detail="Carpool not found")
    return carpool


# Update a carpool
@router.patch("/{carpool_id}", response_model=CarpoolResponse)
def update_carpool(
    carpool_id: int,
    carpool_update: CarpoolUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update an existing carpool (partial update).
    """
    carpool = db.query(Carpool).filter(Carpool.id == carpool_id).first()
    if not carpool:
        raise HTTPException(status_code=404, detail="Carpool not found")

    # Ensure only the owner can update the carpool
    if carpool.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this carpool")

    # Dynamically update fields
    for key, value in carpool_update.dict(exclude_unset=True).items():
        setattr(carpool, key, value)

    db.commit()
    db.refresh(carpool)
    return carpool


# Delete a carpool
@router.delete("/{carpool_id}")
def delete_carpool(
    carpool_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a carpool by its ID.
    """
    carpool = db.query(Carpool).filter(Carpool.id == carpool_id).first()
    if not carpool:
        raise HTTPException(status_code=404, detail="Carpool not found")

    # Ensure only the owner can delete the carpool
    if carpool.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this carpool")

    db.delete(carpool)
    db.commit()
    return {"message": "Carpool deleted successfully"}
