from fastapi import APIRouter, Depends, UploadFile, File, HTTPException,status,Form
from sqlalchemy.orm import Session
from app import models, utils, oauth2
from ..utils import hash
from ..database import get_db
from ..models import User
from ..schemas import user
from datetime import datetime

router = APIRouter(
    tags=['user']
)
@router.post("/signup")
async def user_signup(
    firstName: str = Form(...),
    lastName: str = Form(...),
    phoneNumber: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    gender: str = Form(...),
    profile_picture: UploadFile = File(None),  # Optional file upload
    db: Session = Depends(get_db)
):
    """
    Handles user sign-up with form-data fields and optional image upload.
    """
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Handle the profile picture file
    picture_binary = None
    if profile_picture:
        if profile_picture.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=400, detail="Invalid file format. Only PNG or JPEG allowed.")
        picture_binary = await profile_picture.read()

    # Save user to the database
    new_user = User(
        firstName=firstName,
        lastName=lastName,
        phoneNumber=phoneNumber,
        email=email,
        password=hash(password),
        gender=gender,
        profile_picture=picture_binary  # Store binary data
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}

@router.get("/{id}",response_model=user.UserResponse)
def get_employee(id:int, db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesn\'t exit")
    return user
