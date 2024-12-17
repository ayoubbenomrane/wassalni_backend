from pydantic import BaseModel, EmailStr
from typing import Optional


# Base Schema: Shared properties for User
class UserBase(BaseModel):
    firstName: str
    lastName: str
    phoneNumber: Optional[str] = None
    gender: Optional[str] = None
    email: EmailStr


# Schema for Creating a User (Sign-Up)
class UserCreate(UserBase):
    password: str
    # Profile picture will be handled separately via UploadFile in the route


# Schema for User Response (Exclude Binary Data)
class UserResponse(UserBase):
    id: int
    profile_picture: Optional[bytes] = None  # Omitted from the response for simplicity

    class Config:
        orm_mode = True


# Schema for Retrieving Profile Picture (Binary Data)
class ProfilePictureResponse(BaseModel):
    profile_picture: bytes  # This will hold the binary image data

    class Config:
        orm_mode = True
