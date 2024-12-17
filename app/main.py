# main.py
from fastapi import FastAPI
from app import models
from .database import engine
from .routers import user, auth,carpool

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(auth.router,prefix="/user")
app.include_router(user.router,prefix="/user")
app.include_router(carpool.router,prefix="/carpool")


