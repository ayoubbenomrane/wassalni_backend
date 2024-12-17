from pydantic import BaseModel, EmailStr
from typing import Optional


# Base Schema: Shared properties for User
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    phoneNumber: Optional[str] = None
    email: EmailStr
    password: str
    gender: Optional[str] = None
    profile_picture: Optional[str] = None  # Base64-encoded string

class UserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    phoneNumber: Optional[str] = None
    email: EmailStr
    gender: Optional[str] = None
    profile_picture: Optional[str] = None

    class Config:
        orm_mode = True