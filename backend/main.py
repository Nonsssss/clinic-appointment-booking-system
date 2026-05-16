from fastapi import FastAPI
from appointments import router as appointment_router

app = FastAPI()

app.include_router(appointment_router)


@app.get("/")
def home():
    return {
        "message": "Clinic Backend Running"
    }