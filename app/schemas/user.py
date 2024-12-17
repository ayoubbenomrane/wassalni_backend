from pydantic import BaseModel, EmailStr
from typing import Optional


# Base User schema
class UserBase(BaseModel):
    firstName: str
    lastName: str
    phoneNumber:str
    email: EmailStr
    profile_picture: Optional[str] = None  # Optional field for profile picture URL or path


# Schema for user creation (registration)
class UserCreate(UserBase):
    password: str


# Schema for user response (output)
class UserOut(UserBase):
    class Config:
        orm_mode = True


# Schema for updating user details (e.g., updating phone number, profile picture)
class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None

    class Config:
        orm_mode = True


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
