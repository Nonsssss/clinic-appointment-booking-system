import os
import models
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base, get_db
from models.appointment import Appointment
from schemas.appointment import AppointmentCreate
from sqlalchemy.orm import Session
from routes.auth import router as auth_router
from appointments import router as appointment_router
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="HSU Appointment System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")
app.include_router(appointment_router)

# --- FRONTEND PATHS ---
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BACKEND_DIR, "frontend")
HTML_DIR = os.path.join(FRONTEND_DIR, "html_files")

# --- STATIC FILES ---
# Mount the entire frontend/ folder at /static/
# /static/css/style.css        → frontend/css/style.css
# /static/images/logo2.png     → frontend/images/logo2.png
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- HTML PAGE ROUTES ---
def html(filename: str):
    path = os.path.join(HTML_DIR, filename)
    if not os.path.exists(path):
        return HTMLResponse(f"<h1>404 - {filename} not found</h1><p>Looked in: {path}</p>", status_code=404)
    return FileResponse(path)

@app.get("/")
def home():                         return html("index.html")

@app.get("/login")
def login():                        return html("login.html")

@app.get("/signup")
def signup():                       return html("signup.html")

@app.get("/dashboard")
def dashboard():                    return html("dashboard.html")

@app.get("/booking")
def booking():                      return html("booking.html")

@app.get("/appointments-page")
def appointments_page():            return html("appointments.html")

@app.get("/confirmation")
def confirmation():                 return html("confirmation.html")

@app.get("/admin")
def admin():                        return html("admin-dashboard.html")

@app.get("/admin/approved")
def admin_approved():               return html("admin-approved.html")