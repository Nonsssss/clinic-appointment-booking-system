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
    service_id: int
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
    service = db.query(ServiceModel)\
    .filter(ServiceModel.service_id == payload.service_id)\
    .first()

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
    
    end_datetime = start_datetime + timedelta(minutes=service.duration)
    
    
    
    if start_datetime < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Cannot book an appointment in the past"
        )

    

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
def list_appointments(db: Session = Depends(get_db)):
    # Query appointments and join with the Service model to display legible details
    appointments = db.query(AppointmentModel).all()
    
    results = []
    for app in appointments:
        # Use fallback message if database relations are missing or broken
        service_name = app.service.service_name if app.service else "Unknown Service"
        
        results.append({
            "id": app.appointment_id,
            "patient_name": app.patient_name,
            "date": str(app.appointment_date),  # Yields "YYYY-MM-DD"
            "time": app.start_time.strftime("%I:%M %p"),  # Yields clean 12-hour values like "09:00 AM"
            "service": service_name,
            "status": app.status
        })
        
    return results



@router.get("/appointments/availability/{service_id}/{date}")
def get_availability(service_id: int, date: str, db: Session = Depends(get_db)):
    # 1. Fetch the target service strictly to verify its custom duration length
    service = db.query(ServiceModel).filter(ServiceModel.service_id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # 2. CRITICAL CHANGE: Grab ALL clinic appointments for this date.
    # If the clinic has only 1 doctor, ANY booking blocks the room.
    booked = db.query(AppointmentModel).filter(
        AppointmentModel.appointment_date == date
    ).all()

    booked_slots = []
    for appt in booked:
        start = datetime.combine(appt.appointment_date, appt.start_time)
        end = datetime.combine(appt.appointment_date, appt.end_time)
        booked_slots.append((start, end))

    return {
        "booked": [
            {"start": b[0].isoformat(), "end": b[1].isoformat()}
            for b in booked_slots
        ]
    }


@router.post("/appointments")
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).filter(ServiceModel.service_id == payload.service_id).first()
    if service is None:
        raise HTTPException(status_code=400, detail="Invalid service")

    start_datetime = parse_appointment_start(payload.appointment_date, payload.appointment_time)
    end_datetime = start_datetime + timedelta(minutes=service.duration)
    
    if start_datetime < datetime.now():
        raise HTTPException(status_code=400, detail="Cannot book an appointment in the past")

    # CRITICAL CHANGE: Check overlaps across ALL bookings for that day, regardless of provider or service
    existing_appointments = db.query(AppointmentModel).filter(
        AppointmentModel.appointment_date == start_datetime.date()
    ).all()

    for existing in existing_appointments:
        existing_start = datetime.combine(existing.appointment_date, existing.start_time)
        existing_end = datetime.combine(existing.appointment_date, existing.end_time)

        # Global overlap conflict check
        if start_datetime < existing_end and end_datetime > existing_start:
            raise HTTPException(
                status_code=400,
                detail=f"Clinic is occupied. Next available slot: {existing_end.strftime('%I:%M %p')}"
            )

    # Create the globally validated appointment
    new_appointment = AppointmentModel(
        patient_name=payload.fullname,
        service_id=service.service_id,
        doctor_id=service.doctor_id, # Safely keeps the structural key fallback from DB
        appointment_date=start_datetime.date(),
        start_time=start_datetime.time(),
        end_time=end_datetime.time(),
        status="pending",
        slots_used=1
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {"message": "Appointment booked successfully"}