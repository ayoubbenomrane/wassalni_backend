from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# Base Carpool Schema
class CarpoolBase(BaseModel):
    price: float
    departure: str
    destination: str
    time: datetime
    seats_available: int


# Schema for Creating a Carpool
class CarpoolCreate(CarpoolBase):
    pass


# Schema for Updating a Carpool
class CarpoolUpdate(BaseModel):

    price: Optional[float] = Field(None, gt=0, description="Updated price of the carpool")
    departure: Optional[str] = None
    destination: Optional[str] = None
    time: Optional[datetime] = None
    seats_available: Optional[int] = Field(None, gt=0, description="Updated number of available seats")


# Schema for a Single Carpool Response
class CarpoolResponse(CarpoolBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True


# Schema for a List of Carpools
class CarpoolListResponse(BaseModel):
 
    carpools: List[CarpoolResponse]
    class Config:
        orm_mode = True
