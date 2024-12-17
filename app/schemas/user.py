from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# Base Schema: Shared properties for User
from pydantic import BaseModel, EmailStr
from typing import Optional
class UserBase(BaseModel):
    firstName: str
    lastName: str
    phoneNumber: Optional[str] = None
    profilePicture: Optional[str] = None
    gender: Optional[str] = None
    birthDay: Optional[date] = None
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id:int
    rating:float

    class Config:
        orm_mode = True