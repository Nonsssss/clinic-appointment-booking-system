
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
import os
from fastapi.staticfiles import StaticFiles

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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Mount the frontend folder so the browser can load CSS, JS, and Images
# This makes files like style.css accessible via /static/style.css
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="static")

# Define the paths to your HTML files
INDEX_HTML_PATH = os.path.join(BASE_DIR, "frontend", "index.html")
LOGIN_HTML_PATH = os.path.join(BASE_DIR, "frontend", "login.html")

# 2. Serve index.html as the landing/home page
@app.get("/", response_class=FileResponse)
def get_home_page():
    if not os.path.exists(INDEX_HTML_PATH):
        return {"error": f"index.html not found at {INDEX_HTML_PATH}"}
    return INDEX_HTML_PATH

# 3. Serve login.html
@app.get("/login", response_class=FileResponse)
def get_login_page():
    if not os.path.exists(LOGIN_HTML_PATH):
        return {"error": f"login.html not found at {LOGIN_HTML_PATH}"}
    return LOGIN_HTML_PATH