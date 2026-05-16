from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date, time

router = APIRouter()

# Temporary fake database
appointments = []


class Appointment(BaseModel):
    fullname: str
    service: str
    appointment_date: date
    appointment_time: time


@router.post("/appointments")
def create_appointment(appointment: Appointment):

    # Check double booking
    for existing in appointments:

        if (
            existing["appointment_date"] == appointment.appointment_date
            and existing["appointment_time"] == appointment.appointment_time
        ):
            raise HTTPException(
                status_code=400,
                detail="Time slot already booked"
            )

    appointments.append(appointment.dict())

    return {
        "message": "Appointment booked successfully",
        "data": appointment
    }


@router.get("/appointments")
def get_appointments():
    return appointments