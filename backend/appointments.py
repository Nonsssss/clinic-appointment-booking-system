from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.orm import Session


from database.db import Base, get_db
from models import appointment
from models.appointment import Appointment as AppointmentModel


router = APIRouter()



# Service durations in minutes
SERVICE_DURATIONS = {
    "Medical Clearance": 5,
    "Medical Clearance for Freshmen": 15,
    "Assessment for Internship": 15,
    "Dental Consultation": 20
}


class AppointmentCreate(BaseModel):
    fullname: str
    service: str
    appointment_date: str
    appointment_time: str


@router.post("/appointments")
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):

    # Validate service
    if payload.service not in SERVICE_DURATIONS:
        raise HTTPException(status_code=400, detail="Invalid service")

    duration = SERVICE_DURATIONS[payload.service]

    # Convert input datetime
    start_datetime = datetime.strptime(
        f"{payload.appointment_date} {payload.appointment_time}",
        "%Y-%m-%d %H:%M"
    )

    end_datetime = start_datetime + timedelta(minutes=duration)

    # Get existing appointments
    existing_appointments = db.query(AppointmentModel).all()

    for existing in existing_appointments:

        existing_start = datetime.combine(
            existing.appointment_date,
            existing.start_time
        )

        existing_end = datetime.combine(
            existing.appointment_date,
            existing.end_time
        )

        # Overlap check
        if start_datetime < existing_end and end_datetime > existing_start:
            raise HTTPException(
                status_code=400,
                detail=f"Time conflict. Next available after {existing_end.strftime('%Y-%m-%d %H:%M')}"
            )

    # Create appointment
    new_appointment = AppointmentModel(
        patient_name=payload.fullname,   # FIXED TYPO
        service_id=1,  # TODO: map properly later
        doctor_id=1,
        appointment_date=start_datetime.date(),
        start_time=start_datetime.time(),
        end_time=end_datetime.time(),
        status="pending",
        slots_used=1
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "message": "Appointment booked successfully",
        "appointment": {
            "id": new_appointment.appointment_id,
            "start": str(new_appointment.start_time),
            "end": str(new_appointment.end_time)
        }
    }


@router.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    
    return db.query(AppointmentModel).all()