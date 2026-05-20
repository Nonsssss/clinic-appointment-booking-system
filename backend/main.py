from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from appointments import router as appointment_router
from database.db import engine, Base
import models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(appointment_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Clinic Backend Running and Tables Created!"}
