import os
import models
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base, get_db
from models.appointment import Appointment
from schemas.appointment import AppointmentCreate
from sqlalchemy.orm import Session

# Route Imports
from routes.auth import router as auth_router 
from appointments import router as appointment_router

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="HSU Appointment System")

# CORS Middleware Configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Automatically create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include Routers with explicit prefixes to match your frontend fetches
app.include_router(auth_router, prefix="/auth")
app.include_router(appointment_router, prefix="/api")

# --- FRONTEND ASSET ROUTING SETUP ---

# Get current workspace directory (/app on Railway)
CURRENT_WORKSPACE = os.getcwd() 
FRONTEND_DIR = os.path.join(CURRENT_WORKSPACE, "frontend")

INDEX_HTML_PATH = os.path.join(FRONTEND_DIR, "index.html")
LOGIN_HTML_PATH = os.path.join(FRONTEND_DIR, "login.html")

# 1. Define explicit webpage endpoints first
@app.get("/", response_class=FileResponse)
def get_home_page():
    if not os.path.exists(INDEX_HTML_PATH):
        return {"error": f"index.html not found at {INDEX_HTML_PATH}"}
    return INDEX_HTML_PATH

@app.get("/login", response_class=FileResponse)
def get_login_page():
    if not os.path.exists(LOGIN_HTML_PATH):
        return {"error": f"login.html not found at {LOGIN_HTML_PATH}"}
    return LOGIN_HTML_PATH

# 2. Mount static folder at the very bottom as a fallback option for CSS/JS assets
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")