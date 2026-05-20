from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.orm import Session


from database.db import get_db
from models.appointment import Appointment as AppointmentModel
from models.service import Service as ServiceModel


router = APIRouter()


SERVICE_NAME_ALIASES = {
    "Medical Clearance for University Week": "Medical Clearance for U-Week"
}


class AppointmentCreate(BaseModel):
    fullname: str
    service: str
    appointment_date: str
    appointment_time: str


def parse_appointment_start(appointment_date: str, appointment_time: str):
    raw_datetime = f"{appointment_date} {appointment_time.strip()}"
    accepted_formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %I:%M %p"
    ]

    for date_format in accepted_formats:
        try:
            return datetime.strptime(raw_datetime, date_format)
        except ValueError:
            continue

    raise HTTPException(
        status_code=400,
        detail="Invalid date or time format. Use YYYY-MM-DD with HH:MM or h:mm AM/PM"
    )


@router.post("/appointments")
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    service_name = SERVICE_NAME_ALIASES.get(payload.service, payload.service)

    service = (
        db.query(ServiceModel)
        .filter(ServiceModel.service_name == service_name)
        .first()
    )

    if service is None:
        raise HTTPException(status_code=400, detail="Invalid service")

    if service.duration is None or service.doctor_id is None:
        raise HTTPException(
            status_code=400,
            detail="Selected service is not ready for booking"
        )

    start_datetime = parse_appointment_start(
        payload.appointment_date,
        payload.appointment_time
    )

    if start_datetime < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Cannot book an appointment in the past"
        )

    end_datetime = start_datetime + timedelta(minutes=service.duration)

    existing_appointments = (
        db.query(AppointmentModel)
        .filter(
            AppointmentModel.doctor_id == service.doctor_id,
            AppointmentModel.appointment_date == start_datetime.date()
        )
        .all()
    )

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
        patient_name=payload.fullname,
        service_id=service.service_id,
        doctor_id=service.doctor_id,
        appointment_date=start_datetime.date(),
        start_time=start_datetime.time(),
        end_time=end_datetime.time(),
        status="pending",
        slots_used=service.slots_required or 1
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "message": "Appointment booked successfully",
        "appointment": {
            "id": new_appointment.appointment_id,
            "service_id": new_appointment.service_id,
            "doctor_id": new_appointment.doctor_id,
            "start": str(new_appointment.start_time),
            "end": str(new_appointment.end_time)
        }
    }


@router.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    
    return db.query(AppointmentModel).all()
