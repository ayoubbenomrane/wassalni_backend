from fastapi import APIRouter, Depends, HTTPException
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
@router.post("/", response_model=CarpoolResponse)
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
@router.get("/", response_model=CarpoolListResponse)
def get_all_carpools(db: Session = Depends(get_db)):
    """
    Retrieve a list of all carpools.
    """
    carpools = db.query(Carpool).all()
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
