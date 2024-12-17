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
@router.post("/signup",response_model=user.UserResponse)
def create_user(user:user.UserCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    db.add(models.User(**user.model_dump()))
    db.commit()
    return {**user.model_dump()}

@router.get("/{id}",response_model=user.UserResponse)
def get_employee(id:int, db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesn\'t exit")
    return user
