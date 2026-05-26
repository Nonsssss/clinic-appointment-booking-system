from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional, List

from database.db import get_db
from models.appointment import Appointment as AppointmentModel
from models.service import Service as ServiceModel
from schemas.appointment import AppointmentCreate
from schemas.status import StatusUpdate

router = APIRouter(prefix="/appointments", tags=["appointments"])


def parse_appointment_start(appointment_date: str, appointment_time: str):
    raw_datetime = f"{appointment_date} {appointment_time.strip()}"
    accepted_formats = [
        "%Y-%m-%d %H:%M:%S",    # "2026-05-26 09:00:00"  ← from frontend convertTo24Hour
        "%Y-%m-%d %H:%M",       # "2026-05-26 09:00"
        "%Y-%m-%d %I:%M %p",    # "2026-05-26 9:00 AM"
        "%Y-%m-%d %I:%M:%S %p"  # "2026-05-26 9:00:00 AM"
    ]
    for date_format in accepted_formats:
        try:
            return datetime.strptime(raw_datetime, date_format)
        except ValueError:
            continue
    raise HTTPException(
        status_code=400,
        detail=f"Invalid date or time format received: '{raw_datetime}'"
    )


def serialize_appointment(app: AppointmentModel) -> dict:
    service_name = app.service.service_name if app.service else "Unknown Service"
    return {
        "appointment_id": app.appointment_id,
        "id": app.appointment_id,
        "patient_name": app.patient_name,
        "date": str(app.appointment_date),
        "time": app.start_time.strftime("%I:%M %p") if app.start_time else "N/A",
        "service": service_name,
        "status": app.status,
    }


# ------------------------------------------------------------------
# GET /appointments  — list all, or filter by user_id and/or status
# ------------------------------------------------------------------
@router.get("")
def list_appointments(
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AppointmentModel)
    if user_id is not None:
        query = query.filter(AppointmentModel.user_id == user_id)
    if status is not None:
        query = query.filter(AppointmentModel.status.ilike(status))
    appointments = query.all()
    return [serialize_appointment(a) for a in appointments]


# ------------------------------------------------------------------
# GET /appointments/availability/{service_id}/{date}
# ------------------------------------------------------------------
@router.get("/availability/{service_id}/{date}")
def get_availability(service_id: int, date: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format")

    service = db.query(ServiceModel).filter(ServiceModel.service_id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    booked = db.query(AppointmentModel).filter(
        AppointmentModel.appointment_date == target_date
    ).all()

    booked_slots = []
    for appt in booked:
        # Skip rows with NULL times to avoid crashes on bad/legacy data
        if not appt.start_time or not appt.end_time:
            continue
        start = datetime.combine(appt.appointment_date, appt.start_time)
        end = datetime.combine(appt.appointment_date, appt.end_time)
        booked_slots.append({"start": start.isoformat(), "end": end.isoformat()})

    return {"booked": booked_slots}


# ------------------------------------------------------------------
# GET /appointments/history/{user_id}
# ------------------------------------------------------------------
@router.get("/history/{user_id}")
def get_appointment_history(user_id: int, db: Session = Depends(get_db)):
    appointments = db.query(AppointmentModel).filter(
        AppointmentModel.user_id == user_id
    ).order_by(AppointmentModel.appointment_date.desc()).all()
    return [serialize_appointment(a) for a in appointments]


# ------------------------------------------------------------------
# GET /appointments/processed
# ------------------------------------------------------------------
@router.get("/processed")
def get_processed_appointments(db: Session = Depends(get_db)):
    appointments = db.query(AppointmentModel).filter(
        AppointmentModel.status.notin_(["Pending", "pending"])
    ).all()
    return [serialize_appointment(a) for a in appointments]


# ------------------------------------------------------------------
# POST /appointments
# ------------------------------------------------------------------
@router.post("")
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).filter(ServiceModel.service_id == payload.service_id).first()
    if service is None:
        raise HTTPException(status_code=400, detail="Invalid service")

    start_datetime = parse_appointment_start(payload.appointment_date, payload.appointment_time)
    end_datetime = start_datetime + timedelta(minutes=service.duration)

    if start_datetime < datetime.now():
        raise HTTPException(status_code=400, detail="Cannot book an appointment in the past")

    existing_appointments = db.query(AppointmentModel).filter(
        AppointmentModel.appointment_date == start_datetime.date()
    ).all()

    for existing in existing_appointments:
        # Skip rows with NULL times to avoid crashes
        if not existing.start_time or not existing.end_time:
            continue
        existing_start = datetime.combine(existing.appointment_date, existing.start_time)
        existing_end = datetime.combine(existing.appointment_date, existing.end_time)
        if start_datetime < existing_end and end_datetime > existing_start:
            raise HTTPException(
                status_code=400,
                detail=f"Clinic is occupied. Next available slot: {existing_end.strftime('%I:%M %p')}"
            )

    try:
        new_appointment = AppointmentModel(
            user_id=payload.user_id,
            patient_name=payload.fullname,
            service_id=payload.service_id,
            appointment_date=start_datetime.date(),
            start_time=start_datetime.time(),
            end_time=end_datetime.time(),
            status="pending",
            slots_used=1
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return {"status": "success", "message": "Appointment created"}

    except Exception as e:
        db.rollback()
        print(f"Backend error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ------------------------------------------------------------------
# PUT /appointments/{appointment_id}/status
# ------------------------------------------------------------------
@router.put("/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.get(AppointmentModel, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment record not found.")

    normalized_status = payload.status.strip().capitalize()
    try:
        appointment.status = normalized_status
        db.commit()
        db.refresh(appointment)
        return {"message": f"Status updated to {normalized_status}.", "id": appointment_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to write to database: {str(e)}")