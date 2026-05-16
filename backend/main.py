from fastapi import FastAPI
from appointments import router as appointment_router
from database.db import engine, Base
import models


app = FastAPI()

app.include_router(appointment_router)



@app.get("/")
def home():
    return {
        "message": "Clinic Backend Running"
    }


Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"message": "Clinic Backend Running and Tables Created!"}