
import models
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base, get_db
from models.appointment import Appointment
from schemas.appointment import AppointmentCreate
from sqlalchemy.orm import Session
from routes.auth import router as auth_router # Use this alias cleanly!
from appointments import router as appointment_router
from fastapi.responses import FileResponse


app = FastAPI(title="HSU Appointment System")




app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(appointment_router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGIN_HTML_PATH = os.path.join(BASE_DIR, "frontend", "login.html")

@app.get("/login", response_class=FileResponse)
def get_login_page():
    return LOGIN_HTML_PATH