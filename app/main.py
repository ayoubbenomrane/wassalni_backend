# main.py
from fastapi import FastAPI
from app import models
from .database import engine
from .routers import user, auth,carpool,feedback
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, replace "" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods: GET, POST, PUT, etc.
    allow_headers=["*"],  # Allows all headers
)
# Include routers
app.include_router(auth.router,prefix="/user")
app.include_router(user.router,prefix="/user")
app.include_router(carpool.router,prefix="/carpool")
app.include_router(feedback.router,prefix="/feedback")


